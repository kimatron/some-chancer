document.addEventListener('DOMContentLoaded', function() {
    // Handle quantity input
    const quantityInput = document.getElementById('ticket-quantity');
    const totalPrice = document.getElementById('total-price');
    const ticketPrice = document.getElementById('ticket-price');
    
    if (quantityInput && totalPrice && ticketPrice) {
        const price = parseFloat(ticketPrice.dataset.price);
        
        quantityInput.addEventListener('input', function() {
            const quantity = parseInt(this.value) || 0;
            totalPrice.textContent = (quantity * price).toFixed(2);
        });
    }
    
    // Countdown timer for raffles
    const countdownElements = document.querySelectorAll('.countdown');
    
    countdownElements.forEach(function(element) {
        const endDate = new Date(element.dataset.endDate).getTime();
        
        const timer = setInterval(function() {
            const now = new Date().getTime();
            const distance = endDate - now;
            
            if (distance < 0) {
                clearInterval(timer);
                element.innerHTML = "ENDED";
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            element.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }, 1000);
    });
});