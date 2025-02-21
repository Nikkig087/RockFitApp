from django import forms
import stripe
from datetime import datetime

# Set your Stripe API key
stripe.api_key = "STRIPE_SECRET_KEY"

class CardPaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=13, required=True)
    exp_month = forms.IntegerField(min_value=1, max_value=12, required=True)
    exp_year = forms.IntegerField(min_value=datetime.now().year, required=True)
    cvc = forms.CharField(max_length=4, min_length=3, required=True)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number")
        if not card_number.isdigit():
            raise forms.ValidationError("Card number must be numeric.")
        return card_number

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get("card_number")
        exp_month = cleaned_data.get("exp_month")
        exp_year = cleaned_data.get("exp_year")
        cvc = cleaned_data.get("cvc")
        amount = cleaned_data.get("amount")

        if not all([card_number, exp_month, exp_year, cvc, amount]):
            raise forms.ValidationError("All fields are required.")

        # Check with Stripe for validation
        try:
            token = stripe.Token.create(
                card={
                    "number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                }
            )

            # Attempt a small charge to check funds
            charge = stripe.Charge.create(
                amount=int(amount * 100), # Stripe requires amount in cents
                currency="usd",
                source=token.id,
                description="Card Validation Check",
                capture=False, # This only verifies without charging
            )
            
            if charge["status"] != "succeeded":
                raise forms.ValidationError("Card validation failed. Please check your details.")

        except stripe.error.CardError as e:
            raise forms.ValidationError(f"Card error: {e.user_message}")

        except stripe.error.StripeError as e:
            raise forms.ValidationError(f"Payment processing error: {str(e)}")

        return cleaned_data