
# raffles/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Raffle, Ticket
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    active_raffles = Raffle.objects.filter(is_active=True, end_date__gt=timezone.now())
    featured_raffles = active_raffles.order_by('?')[:4]  # Random selection
    
    return render(request, 'raffles/home.html', {
        'featured_raffles': featured_raffles,
    })

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