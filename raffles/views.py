import stripe
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_q.tasks import async_task
from django.contrib.auth import get_user_model

from .models import Raffle, Ticket, Transaction, Winner, UserProfile
from .utils import select_winner
from .forms import TicketPurchaseForm

User = get_user_model()

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Home Page
@cache_page(settings.CACHE_TIMEOUT)
def home(request):
    """Display the home page with featured raffles."""
    active_raffles = Raffle.objects.filter(is_active=True, end_date__gt=timezone.now())
    
    # Get featured raffles if available, otherwise random selection
    featured_raffles = active_raffles.filter(featured=True)[:4]
    if featured_raffles.count() < 4:
        more_raffles = active_raffles.exclude(id__in=featured_raffles.values_list('id', flat=True))
        featured_raffles = list(featured_raffles) + list(more_raffles[:4-featured_raffles.count()])
    
    return render(request, 'raffles/home.html', {
        'featured_raffles': featured_raffles,
        'now': timezone.now(),
    })

# Raffle Listings
@cache_page(settings.CACHE_TIMEOUT / 2.5)
def raffle_list(request):
    """Display all active and ended raffles."""
    active_raffles = Raffle.objects.filter(
        is_active=True, 
        end_date__gt=timezone.now()
    ).prefetch_related('ticket_set')
    
    ended_raffles = Raffle.objects.filter(
        end_date__lte=timezone.now()
    ).prefetch_related('ticket_set').select_related('winner')
    
    return render(request, 'raffles/raffle_list.html', {
        'active_raffles': active_raffles,
        'ended_raffles': ended_raffles,
        'now': timezone.now(),
    })

# Individual Raffle Details
def raffle_detail(request, raffle_id):
    """Display details of a specific raffle."""
    raffle = get_object_or_404(Raffle, id=raffle_id)
    user_tickets = []
    winner = None
    
    if request.user.is_authenticated:
        user_tickets = Ticket.objects.filter(raffle=raffle, user=request.user)
    
    # Check if the raffle has a winner
    try:
        winner = Winner.objects.get(raffle=raffle)
    except Winner.DoesNotExist:
        pass
    
    return render(request, 'raffles/raffle_detail.html', {
        'raffle': raffle,
        'user_tickets': user_tickets,
        'winner': winner,
        'now': timezone.now(),
    })

# User Authentication
class RegisterView(generic.CreateView):
    """Handle user registration."""
    form_class = UserCreationForm
    success_url = reverse_lazy('raffles:login')
    template_name = 'registration/register.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your account has been created! You can now log in.')
        return response

# User Dashboard
@login_required
def dashboard(request):
    """User dashboard showing tickets, winnings, and account settings."""
    # Get active tickets
    active_tickets = Ticket.objects.filter(
        user=request.user,
        raffle__end_date__gt=timezone.now()
    ).select_related('raffle').order_by('-purchase_date')
    
    # Get past tickets and add a property to show if each ticket was a winner
    past_tickets = Ticket.objects.filter(
        user=request.user,
        raffle__end_date__lte=timezone.now()
    ).select_related('raffle').order_by('-purchase_date')
    
    # Get winning info for past tickets
    winning_tickets = Winner.objects.filter(
        ticket__user=request.user
    ).values_list('ticket_id', flat=True)
    
    # Add is_winner property to past tickets
    for ticket in past_tickets:
        ticket.is_winner = ticket.id in winning_tickets
    
    # Get user winnings
    user_winnings = Winner.objects.filter(
        ticket__user=request.user
    ).select_related('raffle', 'ticket').order_by('-draw_date')
    
    return render(request, 'raffles/dashboard.html', {
        'active_tickets': active_tickets,
        'past_tickets': past_tickets,
        'user_winnings': user_winnings,
    })

@login_required
def update_profile(request):
    """Update user profile information."""
    if request.method == 'POST':
        # Get user and profile
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update user fields
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        # Update profile fields
        profile.phone_number = request.POST.get('phone', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        profile.save()
        
        messages.success(request, 'Your profile has been updated.')
        
    return redirect('raffles:dashboard')

@login_required
def change_password(request):
    """Handle password change requests."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to maintain the session
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('raffles:dashboard')

# Ticket Purchase Flow
@login_required
def purchase_tickets(request, raffle_id):
    """Display the ticket purchase form."""
    raffle = get_object_or_404(Raffle, id=raffle_id)
    
    # Check if raffle is still active
    if not raffle.is_active or raffle.end_date <= timezone.now():
        messages.error(request, "This raffle is no longer available for ticket purchases.")
        return redirect('raffles:raffle_detail', raffle_id=raffle.id)
    
    form = TicketPurchaseForm(raffle=raffle)
    
    return render(request, 'raffles/purchase_tickets.html', {
        'raffle': raffle,
        'form': form,
        'stripe_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def checkout(request, raffle_id):
    """Display the checkout page with summary and payment form."""
    raffle = get_object_or_404(Raffle, id=raffle_id)
    
    # Get quantity from the form
    quantity = int(request.POST.get('quantity', 1))
    
    # Calculate total price
    total_price = raffle.ticket_price * quantity
    
    return render(request, 'raffles/checkout.html', {
        'raffle': raffle,
        'quantity': quantity,
        'total_price': total_price,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
def create_checkout_session(request, raffle_id):
    """Create a Stripe checkout session for payment."""
    raffle = get_object_or_404(Raffle, id=raffle_id)
    
    # Check if raffle is still active
    if not raffle.is_active or raffle.end_date <= timezone.now():
        return JsonResponse({'error': 'This raffle is no longer available'}, status=400)
    
    if request.method == 'POST':
        try:
            # Get quantity from either JSON data or form data
            try:
                data = json.loads(request.body)
                quantity = int(data.get('quantity', 1))
            except json.JSONDecodeError:
                form = TicketPurchaseForm(request.POST, raffle=raffle)
                if form.is_valid():
                    quantity = form.cleaned_data['quantity']
                else:
                    return JsonResponse({'error': 'Invalid form data'}, status=400)
            
            # Check if enough tickets are available
            remaining_tickets = raffle.total_tickets - raffle.tickets_sold
            if quantity > remaining_tickets:
                return JsonResponse({'error': f'Only {remaining_tickets} tickets available'}, status=400)

            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'unit_amount': int(raffle.ticket_price * 100),  # Amount in cents
                            'product_data': {
                                'name': f'Tickets for {raffle.title}',
                                'description': f'{quantity} ticket(s) at €{raffle.ticket_price} each',
                            },
                        },
                        'quantity': quantity,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('raffles:payment_success', kwargs={'raffle_id': raffle.id, 'quantity': quantity})
                ),
                cancel_url=request.build_absolute_uri(reverse('raffles:raffle_detail', kwargs={'raffle_id': raffle.id})),
                metadata={
                    'raffle_id': raffle.id,
                    'user_id': request.user.id,
                    'quantity': quantity
                }
            )
            
            # Create a pending transaction
            transaction = Transaction.objects.create(
                user=request.user,
                raffle=raffle,
                amount=raffle.ticket_price * quantity,
                tickets_purchased=quantity,
                payment_method='credit_card',
                transaction_id=checkout_session.id,
                status='pending'
            )
            
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def process_payment(request, raffle_id):
    """Process the payment after checkout (for non-Stripe payments or testing)."""
    if request.method != 'POST':
        return redirect('raffles:raffle_detail', raffle_id=raffle_id)
    
    raffle = get_object_or_404(Raffle, id=raffle_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # In a real implementation, we would create a Stripe Payment Intent here
    # For demo purposes, we're just redirecting to the success page
    
    return redirect('raffles:payment_success', raffle_id=raffle_id, quantity=quantity)

@login_required
def payment_success(request, raffle_id, quantity):
    """Handle successful payments and ticket generation."""
    raffle = get_object_or_404(Raffle, id=raffle_id)
    total_amount = raffle.ticket_price * quantity
    
    # Update transaction status
    Transaction.objects.filter(
        user=request.user,
        raffle=raffle,
        status='pending'
    ).update(status='completed')
    
    # Generate tickets
    tickets = []
    for _ in range(quantity):
        ticket = Ticket.objects.create(
            raffle=raffle,
            user=request.user
        )
        tickets.append(ticket)
    
    # Update raffle tickets sold count
    raffle.tickets_sold += quantity
    raffle.save()
    
    # Send email with ticket details (async task)
    if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
        async_task('raffles.utils.send_ticket_purchase_email', 
                request.user, 
                raffle, 
                tickets)
    
    return render(request, 'raffles/payment_success.html', {
        'raffle': raffle,
        'quantity': quantity,
        'total_amount': total_amount,
        'tickets': tickets
    })

# Winner Management
@staff_member_required
def draw_winner(request, raffle_id):
    """Draw a winner for a raffle (admin only)."""
    raffle = get_object_or_404(Raffle, id=raffle_id)
    
    # Check if raffle has ended
    if raffle.end_date > timezone.now():
        messages.error(request, "This raffle hasn't ended yet.")
        return redirect('raffles:raffle_detail', raffle_id=raffle.id)
    
    # Check if winner already exists
    try:
        winner = Winner.objects.get(raffle=raffle)
        messages.info(request, "A winner has already been selected for this raffle.")
    except Winner.DoesNotExist:
        # Select a winner
        winner = select_winner(raffle.id)
        
        if winner:
            messages.success(request, f"Winner selected successfully! Ticket #{winner.ticket.ticket_number}")
            
            # Send email notification to winner
            if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                async_task('raffles.utils.send_winner_notification', winner)
        else:
            messages.error(request, "No tickets were sold for this raffle.")
    
    return redirect('raffles:raffle_detail', raffle_id=raffle.id)

@login_required
def claim_prize(request, winner_id):
    """Allow a user to claim their prize."""
    winner = get_object_or_404(Winner, id=winner_id, ticket__user=request.user)
    
    # Mark the prize as claimed
    winner.is_claimed = True
    winner.claim_date = timezone.now()
    winner.save()
    
    messages.success(request, f"Congratulations! Your {winner.raffle.title} prize has been claimed.")
    
    return redirect('raffles:dashboard')

# Winners List View
class WinnersListView(generic.ListView):
    """Display gallery of all winners."""
    model = Winner
    template_name = 'raffles/winners.html'
    context_object_name = 'winners'
    paginate_by = 9
    ordering = ['-draw_date']

# Stripe Webhook Handler
@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events for payment verification."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Extract metadata
        raffle_id = session.get('metadata', {}).get('raffle_id')
        user_id = session.get('metadata', {}).get('user_id')
        quantity = session.get('metadata', {}).get('quantity')
        
        if not all([raffle_id, user_id, quantity]):
            # Missing metadata
            return HttpResponse(status=400)
        
        # Retrieve the transaction
        try:
            transaction = Transaction.objects.get(transaction_id=session.id)
            
            # Update transaction status
            transaction.status = 'completed'
            transaction.save()
            
            # Generate tickets
            raffle = Raffle.objects.get(id=raffle_id)
            user = User.objects.get(id=user_id)
            
            tickets = []
            for _ in range(int(quantity)):
                ticket = Ticket.objects.create(
                    raffle=raffle,
                    user=user
                )
                tickets.append(ticket)
            
            # Update raffle tickets sold count
            raffle.tickets_sold += int(quantity)
            raffle.save()
            
            # Send email notification
            if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                async_task('raffles.utils.send_ticket_purchase_email', user, raffle, tickets)
            
        except (Transaction.DoesNotExist, Raffle.DoesNotExist, User.DoesNotExist) as e:
            # Log the error
            print(f"Error processing webhook: {str(e)}")
            return HttpResponse(status=400)
    
    return HttpResponse(status=200)