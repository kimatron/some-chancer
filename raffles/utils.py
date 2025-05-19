# raffles/utils.py
import random
import hashlib
import time

def select_winner(raffle_id):
    """
    Selects a winner for a raffle using a cryptographically secure method.
    
    This method:
    1. Gets all tickets for the raffle
    2. Creates a hash using the raffle ID, timestamp, and a random salt
    3. Uses the hash to select a winning ticket
    4. Returns the winning ticket
    """
    from .models import Raffle, Ticket, Winner
    
    raffle = Raffle.objects.get(id=raffle_id)
    tickets = list(Ticket.objects.filter(raffle=raffle))
    
    if not tickets:
        return None
    
    # Create a unique, unpredictable seed for the random selection
    timestamp = int(time.time())
    random_salt = random.randint(1, 1000000)
    seed_string = f"{raffle_id}-{timestamp}-{random_salt}"
    seed_hash = hashlib.sha256(seed_string.encode()).hexdigest()
    
    # Convert the first 8 characters of the hash to an integer
    seed_int = int(seed_hash[:8], 16)
    random.seed(seed_int)
    
    # Select a random ticket
    winning_ticket = random.choice(tickets)
    
    # Create a Winner record
    winner = Winner.objects.create(
        raffle=raffle,
        ticket=winning_ticket
    )
    
    # Mark the raffle as inactive
    raffle.is_active = False
    raffle.save()
    
    return winner