/* jslint esversion: 6 */
/* global $ */

var contactFormUrl = "{% url 'contact_form' %}";

(function () {
    if (window.contactScriptInitialized) {
        console.log("Contact script already initialized. Skipping.");
        return;
    }

    window.contactScriptInitialized = true;
    console.log("Initializing contact script at", (new Date()).toISOString());

    $("#contactButton").off("click").on("click", function () {
        console.log("Contact button clicked at", (new Date()).toISOString());
        $("#contactModal").modal("show");

        $.ajax({
            url: contactFormUrl,
            type: "GET",
            success: function (data) {
                console.log("Contact form loaded successfully at", (new Date()).toISOString());
                $("#contactModal .modal-body").html(data);
            },
            error: function (xhr, status, error) {
                console.error("AJAX request failed:", status, error);
                $("#contactModal .modal-body").html("<p>There was an error loading the form.</p>");
            }
        });
    });

    $(document).off("submit", "#contactForm").on("submit", "#contactForm", function (event) {
        event.preventDefault();
        console.log("Contact form submitted at", (new Date()).toISOString());

        var $form = $(this);
        var $submitButton = $form.find('button[type="submit"]');

        if ($submitButton.data("submitting")) {
            console.log("Form already submitting, ignoring request");
            return;
        }

        $submitButton.data("submitting", true);

        $.ajax({
            url: $form.attr("action"),
            type: "POST",
            data: $form.serialize(),
            success: function (response) {
                console.log("Contact form submission successful at", (new Date()).toISOString(), response);
                $("#contactModal .modal-body").html(`
                    <div class="contact">
                        <h5>Thank You!</h5>
                        <p class="contact">Thank you for contacting us. A member of our team will be in touch soon!</p>
                    </div>
                `);
                setTimeout(function () {
                    $("#contactModal").modal("hide");
                    console.log("Contact modal hidden at", (new Date()).toISOString());
                }, 2000);
            },
            error: function (xhr, status, error) {
                console.error("Contact form submission failed:", status, error);
                $("#contactModal .modal-body").html("<p>There was an error with your submission.</p>");
            },
            complete: function () {
                $submitButton.data("submitting", false);
            }
        });
    });

    $("#contactModal").on("hidden.bs.modal", function () {
        console.log("Contact modal hidden at", (new Date()).toISOString());
        var modalBody = $(this).find(".modal-body");
        modalBody.html("");
    });
})();
