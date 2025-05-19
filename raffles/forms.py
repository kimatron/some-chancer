from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="You must purchase at least 1 ticket."),
            MaxValueValidator(100, message="You cannot purchase more than 100 tickets at once.")
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100})
    )
    
    def __init__(self, *args, **kwargs):
        self.raffle = kwargs.pop('raffle', None)
        super().__init__(*args, **kwargs)
        
        if self.raffle:
            remaining_tickets = self.raffle.total_tickets - self.raffle.tickets_sold()
            self.fields['quantity'].validators.append(
                MaxValueValidator(remaining_tickets, message=f"Only {remaining_tickets} tickets available.")
            )