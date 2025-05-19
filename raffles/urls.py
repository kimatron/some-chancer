# raffles/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'raffles'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('raffles/', views.raffle_list, name='raffle_list'),
    path('raffle/<int:raffle_id>/', views.raffle_detail, name='raffle_detail'),
    path('winners/', views.WinnersListView.as_view(), name='winners'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update-profile/', views.update_profile, name='update_profile'),
    path('dashboard/change-password/', views.change_password, name='change_password'),
    
    # Purchase flow
    path('raffle/<int:raffle_id>/purchase/', views.purchase_tickets, name='purchase_tickets'),
    path('raffle/<int:raffle_id>/checkout/', views.checkout, name='checkout'),
    path('raffle/<int:raffle_id>/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('raffle/<int:raffle_id>/process-payment/', views.process_payment, name='process_payment'),
    path('payment/success/<int:raffle_id>/<int:quantity>/', views.payment_success, name='payment_success'),
    
    # Admin actions
    path('raffle/<int:raffle_id>/draw-winner/', views.draw_winner, name='draw_winner'),
    
    # Prize claiming
    path('claim-prize/<int:winner_id>/', views.claim_prize, name='claim_prize'),
    
    # Stripe webhook
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]