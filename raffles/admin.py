from django.contrib import admin
from .models import Raffle, Ticket

@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ('title', 'ticket_price', 'total_tickets', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'start_date', 'end_date')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'raffle', 'user', 'purchase_date')
    search_fields = ('ticket_number', 'user__username', 'raffle__title')
    list_filter = ('purchase_date', 'raffle')