from django.db import models
from django.contrib.auth.models import User
import uuid

class Raffle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='raffle_images/', blank=True, null=True)
    total_tickets = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def tickets_sold(self):
        return self.ticket_set.count()
    
    def __str__(self):
        return self.title

class Ticket(models.Model):
    ticket_number = models.CharField(max_length=50, unique=True)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = str(uuid.uuid4())[:8].upper()
        super(Ticket, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_number} - {self.raffle.title}"
      
class Transaction(models.Model):
    PAYMENT_METHODS = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tickets_purchased = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
      
class Winner(models.Model):
    raffle = models.OneToOneField(Raffle, on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    draw_date = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)
    claim_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Winner of {self.raffle.title}: {self.ticket.user.username}"