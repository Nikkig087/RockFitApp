/* jshint esversion: 6 */
/* global $ */
var contactFormUrl = "{% url 'contact_form' %}";
(function() {
    if (window.contactScriptInitialized) {
        console.log('Contact script already initialized. Skipping.');
        return;
    }
    window.contactScriptInitialized = true;

    console.log('Initializing contact script at', new Date().toISOString());

    // Contact Form Modal Logic
    $('#contactButton').off('click').on('click', function () {
        console.log('Contact button clicked at', new Date().toISOString());
        $('#contactModal').modal('show');
        // Load the contact form via AJAX
        $.ajax({
            url: contactFormUrl, // Use the URL variable defined in the template
            type: 'GET',
            success: function (data) {
                console.log('Contact form loaded successfully at', new Date().toISOString());
                $('#contactModal .modal-body').html(data);
            },
            error: function (xhr, status, error) {
                console.error("AJAX request failed:", status, error);
                $('#contactModal .modal-body').html('<p>There was an error loading the form.</p>');
            }
        });
    });

    // Contact Form Submission Logic
    $(document).off('submit', '#contactForm').on('submit', '#contactForm', function (event) {
        event.preventDefault();
        console.log('Contact form submitted at', new Date().toISOString());

        var $form = $(this);
        var $submitButton = $form.find('button[type="submit"]');

        if ($submitButton.data('submitting')) {
            console.log('Form already submitting, ignoring request');
            return; // Prevent multiple submissions
        }

        $submitButton.data('submitting', true); // Set submitting flag

        $.ajax({
            url: $form.attr('action'),
            type: 'POST',
            data: $form.serialize(),
            success: function (response) {
                console.log('Contact form submission successful at', new Date().toISOString(), response);
                $('#contactModal .modal-body').html('<h5>Thank You!</h5><p>Thank you for contacting us!</p>');
                setTimeout(function () {
                    $('#contactModal').modal('hide'); // Hide the modal
                    console.log('Contact modal hidden at', new Date().toISOString());
                }, 2000); // Delay to show the thank-you message
            },
            error: function (xhr, status, error) {
                console.error("Contact form submission failed:", status, error);
                $('#contactModal .modal-body').html('<p>There was an error with your submission.</p>');
            },
            complete: function () {
                $submitButton.data('submitting', false); // Reset flag
            }
        });
    });

    // Reset contact modal content when hidden
    $('#contactModal').on('hidden.bs.modal', function () {
        console.log('Contact modal hidden at', new Date().toISOString());
        var modalBody = $(this).find('.modal-body');
        modalBody.html(''); // Clear the content to ensure it loads fresh next time
    });
})();