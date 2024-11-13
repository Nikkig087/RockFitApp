// Get CSRF token from the page (from the hidden form field injected by Django)
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Example function to send data using AJAX
function addPlans() {
    const plans = [
        {
            name: "Basic Plan",
            price: "10.00",
            duration: 30,
            benefits: "Basic benefits"
        },
        {
            name: "Premium Plan",
            price: "20.00",
            duration: 60,
            benefits: "Premium benefits"
        },
        {
            name: "Gold Plan",
            price: "40.00",
            duration: 60,
            benefits: "Gold benefits"
        }
    ];

    // Make the AJAX POST request with CSRF token
    fetch('/add-plans/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Include CSRF token in the header
        },
        body: JSON.stringify({
            plans: plans
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Plans added:", data);
    })
    .catch(error => {
        console.error("Error adding plans:", error);
    });
}
