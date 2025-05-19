from django.urls import path
from . import views

app_name = 'raffles'

urlpatterns = [
    path('', views.home, name='home'),
    path('raffles/', views.raffle_list, name='raffle_list'),
    path('raffle/<int:raffle_id>/', views.raffle_detail, name='raffle_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('raffle/<int:raffle_id>/purchase/', views.purchase_tickets, name='purchase_tickets'),
path('raffle/<int:raffle_id>/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
path('payment/success/<int:raffle_id>/<int:quantity>/', views.payment_success, name='payment_success'),
path('raffle/<int:raffle_id>/draw-winner/', views.draw_winner, name='draw_winner'),
]