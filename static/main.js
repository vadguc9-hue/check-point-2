// --- Enhancement 1: Delete Confirmation ---
function confirmDelete(recipeName) {
    return confirm(`Are you sure you want to delete "${recipeName}"? This action cannot be undone.`);
}

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Enhancement 2: Auto-hide Flash Messages (3 Second Timer) ---
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Wait 3 seconds
        setTimeout(() => {
            // Smooth fade out transition
            alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            
            // Remove from the page entirely after fade finishes
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 3000); 
    });

    // --- Enhancement 3: Form Validation Feedback ---
    const form = document.querySelector('.recipe-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            if (nameInput.value.trim() === "") {
                e.preventDefault();
                nameInput.style.borderColor = "var(--danger)";
                // Shake animation for error
                nameInput.classList.add('shake');
                setTimeout(() => nameInput.classList.remove('shake'), 500);
            }
        });
    }

    // --- Enhancement 4: Staggered Entrance Animation for Cards ---
    const cards = document.querySelectorAll('.recipe-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.4s ease-out';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index); // Stagger effect
    });
});