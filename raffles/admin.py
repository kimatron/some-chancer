from django.contrib import admin
from .models import Raffle, Ticket

@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ('title', 'ticket_price', 'total_tickets', 'tickets_sold', 'is_active', 'featured', 'end_date')
    list_filter = ('is_active', 'featured', 'end_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Raffle Information', {
            'fields': ('title', 'description', 'image', 'total_tickets', 'ticket_price')
        }),
        ('Status', {
            'fields': ('is_active', 'featured', 'tickets_sold')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'created_at')
        }),
    )

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'raffle', 'user', 'purchase_date')
    search_fields = ('ticket_number', 'user__username', 'raffle__title')
    list_filter = ('purchase_date', 'raffle')