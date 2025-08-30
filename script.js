// Auto-hide flash messages
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Booking page functionality
if (document.getElementById('bookingForm')) {
    // Set minimum date to tomorrow
    const dateInput = document.getElementById('date');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    dateInput.min = tomorrow.toISOString().split('T')[0];

    // Check availability when date changes
    async function checkAvailability() {
        const date = dateInput.value;
        const timeSelect = document.getElementById('time');
        
        if (!date) {
            timeSelect.innerHTML = '<option value="">Select date first...</option>';
            return;
        }
        
        timeSelect.innerHTML = '<option value="">Loading...</option>';
        
        try {
            const response = await fetch(`/api/availability/${date}`);
            const data = await response.json();
            
            timeSelect.innerHTML = '<option value="">Select a time...</option>';
            
            if (data.available && data.times.length > 0) {
                data.times.forEach(time => {
                    const option = document.createElement('option');
                    option.value = time;
                    option.textContent = time;
                    timeSelect.appendChild(option);
                });
            } else {
                timeSelect.innerHTML = '<option value="">No availability</option>';
            }
        } catch (error) {
            timeSelect.innerHTML = '<option value="">Error loading times</option>';
            console.error('Error checking availability:', error);
        }
    }

    // Update pricing display
    function updatePricing() {
        const serviceSelect = document.getElementById('service');
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        const pricingSummary = document.getElementById('pricingSummary');
        
        if (selectedOption.value) {
            const serviceName = selectedOption.value;
            const servicePrice = selectedOption.dataset.price;
            
            document.getElementById('selectedService').textContent = serviceName;
            document.getElementById('servicePrice').textContent = servicePrice;
            
            calculateTotal();
            pricingSummary.style.display = 'block';
        } else {
            pricingSummary.style.display = 'none';
        }
    }

    // Calculate total with additional services
    function calculateTotal() {
        const serviceSelect = document.getElementById('service');
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        const additionalCheckboxes = document.querySelectorAll('input[name="additional[]"]:checked');
        const additionalContainer = document.getElementById('additionalServices');
        
        let basePrice = 0;
        let additionalTotal = 0;
        
        // Extract base price
        if (selectedOption.value) {
            const priceText = selectedOption.dataset.price;
            // Extract numeric value from price string
            basePrice = parseInt(priceText.replace(/\D/g, ''));
        }
        
        // Clear additional services display
        additionalContainer.innerHTML = '';
        
        // Add additional services
        additionalCheckboxes.forEach(checkbox => {
            const value = checkbox.value;
            let price = 0;
            
            if (value === 'mixing') price = 75;
            else if (value === 'mastering') price = 50;
            else if (value === 'stems') price = 25;
            
            additionalTotal += price;
            
            const div = document.createElement('div');
            div.className = 'd-flex justify-content-between mb-2';
            div.innerHTML = `
                <span>+ ${value.charAt(0).toUpperCase() + value.slice(1)}:</span>
                <span>$${price}</span>
            `;
            additionalContainer.appendChild(div);
        });
        
        const total = basePrice + additionalTotal;
        document.getElementById('totalPrice').textContent = `$${total}`;
    }

    // Add event listeners to additional service checkboxes
    document.querySelectorAll('input[name="additional[]"]').forEach(checkbox => {
        checkbox.addEventListener('change', calculateTotal);
    });

    // Form validation and submission
    document.getElementById('bookingForm').addEventListener('submit', function(e) {
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const service = document.getElementById('service').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const description = document.getElementById('description').value;
        
        if (!name || !email || !service || !date || !time || !description) {
            e.preventDefault();
            alert('Please fill in all required fields.');
            return;
        }
        
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
        submitBtn.disabled = true;
        
        // Reset button after a delay (in case of errors)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 5000);
    });

    // File upload validation
    document.getElementById('reference').addEventListener('change', function(e) {
        const files = e.target.files;
        const maxSize = 10 * 1024 * 1024; // 10MB
        
        for (let file of files) {
            if (file.size > maxSize) {
                alert(`File "${file.name}" is too large. Maximum size is 10MB.`);
                e.target.value = '';
                break;
            }
        }
    });

    // Add event listeners
    document.getElementById('date').addEventListener('change', checkAvailability);
    document.getElementById('service').addEventListener('change', updatePricing);
}

// Portfolio page functionality
if (document.querySelector('.play-btn')) {
    // Play button functionality
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const trackId = this.dataset.track;
            const icon = this.querySelector('i');
            
            // Toggle play/pause
            if (icon.classList.contains('fa-play')) {
                icon.classList.remove('fa-play');
                icon.classList.add('fa-pause');
                
                // Stop other tracks
                document.querySelectorAll('.play-btn i').forEach(otherIcon => {
                    if (otherIcon !== icon) {
                        otherIcon.classList.remove('fa-pause');
                        otherIcon.classList.add('fa-play');
                    }
                });
                
                console.log(`Playing track ${trackId}`);
                // Here you would implement actual audio playback
            } else {
                icon.classList.remove('fa-pause');
                icon.classList.add('fa-play');
                console.log(`Pausing track ${trackId}`);
            }
        });
    });

    // Filter animation
    document.querySelectorAll('a[href*="genre="]').forEach(link => {
        link.addEventListener('click', function(e) {
            // Add loading animation
            const container = document.querySelector('.container .row');
            if (container) {
                container.style.opacity = '0.5';
                container.style.transition = 'opacity 0.3s ease';
            }
        });
    });
}