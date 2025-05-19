from django.urls import path
from . import views

app_name = 'raffles'

urlpatterns = [
    path('', views.home, name='home'),
    path('raffles/', views.raffle_list, name='raffle_list'),
    path('raffle/<int:raffle_id>/', views.raffle_detail, name='raffle_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
]