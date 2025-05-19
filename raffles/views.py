import stripe
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Raffle, Ticket, Transaction, Winner
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .utils import select_winner 
from .forms import TicketPurchaseForm
from django.views.decorators.cache import cache_page
from django.conf import settings


@cache_page(settings.CACHE_TIMEOUT)
def home(request):
    active_raffles = Raffle.objects.filter(is_active=True, end_date__gt=timezone.now())
    featured_raffles = active_raffles.order_by('?')[:4]  # Random selection
    
    return render(request, 'raffles/home.html', {
        'featured_raffles': featured_raffles,
    })

@cache_page(settings.CACHE_TIMEOUT / 2.5)
def raffle_list(request):
    active_raffles = Raffle.objects.filter(is_active=True, end_date__gt=timezone.now())
    ended_raffles = Raffle.objects.filter(end_date__lte=timezone.now())
    
    return render(request, 'raffles/raffle_list.html', {
        'active_raffles': active_raffles,
        'ended_raffles': ended_raffles,
    })

def raffle_detail(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)
    user_tickets = []
    
    if request.user.is_authenticated:
        user_tickets = Ticket.objects.filter(raffle=raffle, user=request.user)
    
    return render(request, 'raffles/raffle_detail.html', {
        'raffle': raffle,
        'user_tickets': user_tickets,
    })
    
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
    
@login_required
def user_dashboard(request):
    user_tickets = Ticket.objects.filter(user=request.user).order_by('-purchase_date')
    active_tickets = user_tickets.filter(raffle__end_date__gt=timezone.now())
    ended_tickets = user_tickets.filter(raffle__end_date__lte=timezone.now())
    
    return render(request, 'raffles/dashboard.html', {
        'active_tickets': active_tickets,
        'ended_tickets': ended_tickets,
    })

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def purchase_tickets(request, raffle_id):
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
def create_checkout_session(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)
    
    # Check if raffle is still active
    if not raffle.is_active or raffle.end_date <= timezone.now():
        return JsonResponse({'error': 'This raffle is no longer available'}, status=400)
    
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST, raffle=raffle)
        
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Check if enough tickets are available
            remaining_tickets = raffle.total_tickets - raffle.tickets_sold()
            if quantity > remaining_tickets:
                return JsonResponse({'error': f'Only {remaining_tickets} tickets available'}, status=400)

            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'eur',
                                'unit_amount': int(raffle.ticket_price * 100),
                                'product_data': {
                                    'name': f'Ticket(s) for {raffle.title}',
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

    return JsonResponse({'error': 'Invalid request or invalid form data'}, status=400)


@login_required
def payment_success(request, raffle_id, quantity):
    raffle = get_object_or_404(Raffle, id=raffle_id)
    
    # Update transaction status
    # In a real application, you'd verify the payment with Stripe's webhook
    # This is simplified for the tutorial
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
    
    return render(request, 'raffles/payment_success.html', {
        'raffle': raffle,
        'quantity': quantity,
        'total_amount': raffle.ticket_price * quantity,
        'tickets': tickets
    })    
    
@staff_member_required
def draw_winner(request, raffle_id):
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
        # For now, we'll add a placeholder
        messages.success(request, "Winner selection will be implemented in Phase 5.")
    
    return redirect('raffles:raffle_detail', raffle_id=raffle.id)
  

def raffle_list(request):
    # Use select_related to reduce database queries
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
    })

@login_required
def user_dashboard(request):
    # Use select_related to reduce database queries
    user_tickets = Ticket.objects.filter(
        user=request.user
    ).select_related('raffle').order_by('-purchase_date')
    
    active_tickets = [t for t in user_tickets if t.raffle.end_date > timezone.now()]
    ended_tickets = [t for t in user_tickets if t.raffle.end_date <= timezone.now()]
    
    return render(request, 'raffles/dashboard.html', {
        'active_tickets': active_tickets,
        'ended_tickets': ended_tickets,
    })