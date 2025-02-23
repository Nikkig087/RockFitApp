from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from fitness.models import Product, SubscriptionPlan, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


import stripe
import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Order

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
#from .models import Cart, Order, OrderItem, SubscriptionPlan, UserProfile

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseServerError
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Cart, Order, CartItem

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
from .models import Cart, Order, OrderItem

@login_required
def payment_success(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    # Freeze the items into a list so they remain available after deletion
    cart_items = list(cart.items.all())

    # Construct the order details for the email
    order_details = "Here is your order summary:\n\n"
    for item in cart_items:
        if item.product:
            order_details += f"- {item.product.name} (x{item.quantity}) - €{item.get_cost():.2f}\n"
        elif item.subscription:
            order_details += f"- {item.subscription.name} (Subscription, x{item.quantity}) - €{item.get_cost():.2f}\n"

    total_cost = cart.get_total_cost()
    order_details += f"\nTotal Amount: €{total_cost:.2f}\n"

    # Debug output
    print("ORDER DETAILS FOR EMAIL:")
    print(order_details)

    # Send confirmation email with the order details
    send_mail(
        subject="Order Confirmation - Rockfit",
        message=(
            f"Dear {user.username},\n\n"
            "Thank you for your purchase!\n\n"
            f"{order_details}\n\n"
            "Enjoy your order!\nRockfit Team"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    # Now clear the cart items
    cart.items.all().delete()

    return render(request, "cart/success.html", {"order_total": total_cost})


# Checkout Page
from django.shortcuts import render, get_object_or_404
from .models import Order

def checkout(request, order_id):
    """
    Display the checkout page where the user can proceed with payment.
    """
    order = get_object_or_404(Order, id=order_id)

    # If the order exists, render the checkout page (use order details as needed)
    return render(request, 'cart/checkout.html', {'order': order})


import stripe
import json
import logging
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from .models import Order

# Initialize logger
logger = logging.getLogger(__name__)

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import render, redirect
from django.http import JsonResponse
import stripe
import json
from .models import Order  # Import the Order model
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY  # Your Stripe secret key from environment variables

from django.http import JsonResponse
import stripe
from django.conf import settings
from .models import Order


# Set your secret key from Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

import stripe
import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags

stripe.api_key = settings.STRIPE_SECRET_KEY

import stripe
import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order, CartItem  # Adjust the import to your actual model if needed

stripe.api_key = settings.STRIPE_SECRET_KEY
import stripe
import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Order  # Adjust the import to your actual model

stripe.api_key = settings.STRIPE_SECRET_KEY

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
import json
from .models import Order
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.core.mail import send_mail
''''
def send_success_email(order):
    subject = "Your Order Has Been Confirmed!"
    message = f"""
    Hi {order.full_name},  

    Thank you for your purchase! Your order #{order.id} has been successfully placed.  

    Order Summary:  
    ------------------------  
    {format_order_items(order)}  
    ------------------------  

    Total Paid: €{order.total_price}  

    Your order will be processed shortly.  

    Thanks for shopping with us!  
    RockFit Team
    """
    send_mail(subject, message, "noreply@rockfit.com", [order.user.email])

def format_order_items(order):
    return "\n".join(
        [f"{item.quantity}x {item.product.name} - €{item.product.price * item.quantity}" for item in order.items.all()]
    )

'''
def send_failed_email(email, error_message):
    subject = "Payment Failed"
    message = f"Your payment attempt failed with the following error: {error_message}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

import json
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Cart, Order, CartItem
#from .emails import send_success_email  # Import the email function

stripe.api_key = settings.STRIPE_SECRET_KEY

# views.py
from .models import Order, OrderItem, CartItem, Cart
from django.core.mail import send_mail

from django.http import JsonResponse
from .models import Order, OrderItem, Cart, CartItem
import stripe

# Your stripe secret key setup
stripe.api_key = 'your-stripe-secret-key'

def process_payment(request):
    data = json.loads(request.body)
    payment_method_id = data.get("payment_method_id")
    email = data.get("email")
    full_name = data.get("full_name")

    try:
        # Get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_cost(),
            status='pending',
            full_name=full_name,
            email=email
        )

        # Create the order items
        for cart_item in cart.items.all():
            print(f"DEBUG - Cart Item: {cart_item}")
            print(f"DEBUG - Product: {cart_item.product} (Type: {type(cart_item.product)})")

            if isinstance(cart_item.product, Product):
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            elif cart_item.subscription:
                OrderItem.objects.create(
                    order=order,
                    subscription=cart_item.subscription,
                    quantity=cart_item.quantity
                )

        # Create Stripe PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.total_price * 100),  # Convert to cents
            currency="eur",
            payment_method=payment_method_id,
            confirmation_method="manual",
            confirm=True,
            return_url=request.build_absolute_uri(reverse("cart:success")),  # Redirect URL after payment success
        )

        # Clear the cart after successful payment intent creation
        cart.items.all().delete()  

        # Return success response with client_secret
        return JsonResponse({"status": "success", "client_secret": payment_intent.client_secret})

    except stripe.error.CardError as e:
        send_failed_email(email, str(e))
        return JsonResponse({"status": "failed", "error": str(e)})

    except Exception as e:
        send_failed_email(email, str(e))
        return JsonResponse({"status": "failed", "error": str(e)})


##return JsonResponse({"status": "success", "client_secret": payment_intent.client_secret})

    except stripe.error.CardError as e:
        send_failed_email(email, str(e))  # Send failure email with the general error message
        return JsonResponse({"status": "failed", "error": str(e)})

    except Exception as e:
        send_failed_email(email, str(e))  # Send failure email with the general error message
        return JsonResponse({"status": "failed", "error": str(e)})




'''
def send_success_email(email, order):
    subject = "Your Order Payment Was Successful"
    message = f"Dear Customer,\n\nYour payment for Order #{order.id} was successful. Total: €{order.total_price}. Thank you for your purchase!"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def send_failed_email(email, order=None):
    subject = "Payment Failed for Your Order"
    message = "Dear Customer,\n\nUnfortunately, your payment has failed. Please try again or contact support."
    if order:
        message += f"\n\nOrder Details: Order #{order.id} with total €{order.total_price}."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order
from decimal import Decimal

@login_required(login_url="login")
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    # Calculate the total cost and delivery fee as needed
    total_cost = sum(
        (item.product.price if item.product else item.subscription.price) * item.quantity
        for item in cart_items
    )
    
    delivery_fee = Decimal("5.00") if total_cost < Decimal("50.00") else Decimal("0.00")
    final_total = total_cost + delivery_fee

    # Retrieve the pending order (if any) for the logged-in user
    order = Order.objects.filter(user=request.user, status="pending").first()

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "total_cost": total_cost,
            "delivery_fee": delivery_fee,
            "final_total": final_total,
            "order": order,  # Pass order to template for checkout button
        },
    )

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, SubscriptionPlan, Cart, CartItem
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, SubscriptionPlan, Cart, CartItem

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, SubscriptionPlan, Cart, CartItem
from fitness.models import Product  # Ensure this import is present

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, SubscriptionPlan, Cart, CartItem


def add_to_cart(request, item_id, item_type):
    from fitness.models import Product  # Ensure import
    print(f"Item ID: {item_id}, Item Type: {item_type}")
    
    # Debugging: Print all products
    print("Available product IDs:", list(Product.objects.values_list("id", flat=True)))
    
    if item_type == "product":
        item = get_object_or_404(Product, id=item_id)  # Error happens here

    print(f"Item ID: {item_id}, Item Type: {item_type}")  # Debugging
    if item_type == "product":
        item = get_object_or_404(Product, id=item_id)
    elif item_type == "subscription":
        return add_subscription_to_cart(request, item_id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect("fitness:products") 
    
    # Rest of your function...

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        if item_type == "product":
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item)
            if not created:
                cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f"{item.name} has been added to your cart!")
    else:
        cart = request.session.get("cart", {})
        key = f"{item_type}_{item_id}"
        if key in cart:
            cart[key]["quantity"] += 1
        else:
            cart[key] = {"type": item_type, "quantity": 1}
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Item added to your cart!")
    
    # Corrected the redirection to use proper names
    return redirect("fitness:products" if item_type == "product" else "fitness:subscription_plans")
'''
@login_required
def process_payment(request):
    """
    Process the payment using Stripe and redirect accordingly.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Assume `payment_intent_id` is stored in session
        payment_intent_id = request.session.get("payment_intent_id")
        if not payment_intent_id:
            messages.error(request, "Payment session expired. Please try again.")
            return redirect("cart:cart_view")

        # Retrieve payment status
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if payment_intent.status == "succeeded":
            return redirect("cart:payment_success")
        else:
            return redirect("cart:payment_failed")

    except stripe.error.CardError as e:
        messages.error(request, "Your card was declined. Please try another payment method.")
        return redirect("cart:payment_failed")

    except stripe.error.StripeError as e:
        messages.error(request, "Payment processing error. Please try again.")
        return redirect("cart:payment_failed")

    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        return redirect("cart:payment_failed")
'''
@login_required
def remove_from_cart(request, cart_item_id):
    """
    Remove an item from the user's cart.

    Deletes the specified cart item from the user's cart.
    The cart item is identified by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_item_id (int): The ID of the cart item to be removed.

    Returns:
        HttpResponse: Redirects to the cart view after removal.
    """
    cart_item = get_object_or_404(
        CartItem, id=cart_item_id, cart__user=request.user
    )
    cart_item.delete()
    messages.success(request, "Item removed from your cart!")
    return redirect("cart:view_cart")


@login_required
def update_cart_item(request, cart_item_id):
    """
    Update the quantity of an item in the user's cart.

    Handles POST requests to update the quantity of a specified cart item.
    The new quantity is provided in the POST data.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_item_id (int): The ID of the cart item to update.

    Returns:
        HttpResponse: Redirects to the cart view after updating the item.
    """
    cart_item = get_object_or_404(
        CartItem, id=cart_item_id, cart__user=request.user
    )

    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity"))
        if new_quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Items updated in your cart!")
    
    return redirect("cart:view_cart")


stripe.api_key = settings.STRIPE_SECRET_KEY

'''
def create_checkout_session(request):
    """
    Create a Stripe checkout session with the user's cart items.
    """
    cart = get_object_or_404(Cart, user=request.user)

    subscription_plan = None
    line_items = []
    total_cost = 0

    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:view_cart")  # Redirect back to cart view if empty

    for item in cart.items.all():
        if item.product:
            item_total = item.product.price * item.quantity
            total_cost += item_total
            line_items.append(
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": item.product.name,
                        },
                        "unit_amount": int(item.product.price * 100),
                    },
                    "quantity": item.quantity,
                }
            )
        elif item.subscription:
            subscription_plan = item.subscription
            item_total = item.subscription.price
            total_cost += item_total
            line_items.append(
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": item.subscription.name,
                        },
                        "unit_amount": int(item.subscription.price * 100),
                    },
                    "quantity": 1,
                }
            )

    if subscription_plan:
        request.session["selected_plan_id"] = subscription_plan.id
    
    try:
        success_url = request.build_absolute_uri(reverse("cart:success"))
        cancel_url = request.build_absolute_uri(reverse("cart:cancel"))

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=request.user.id,
        )

        return redirect(checkout_session.url)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
'''
'''
@login_required
def payment_success(request):
    """
    Handle the successful payment response from Stripe and
    update the user's subscription.
    """
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()  # Clear the cart after successful payment

    subscription_plan_id = request.session.get("selected_plan_id")
    if subscription_plan_id:
        plan = get_object_or_404(SubscriptionPlan, id=subscription_plan_id)
        user_profile = request.user.userprofile
        user_profile.subscription_plan = plan
        user_profile.subscription_start_date = timezone.now()
        user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=plan.duration)
        user_profile.save()

        messages.success(request, f"Successfully subscribed to the {plan.name} plan!")
        del request.session["selected_plan_id"]

        

    return render(request, "cart/payment_success.html")
'''
'''
@login_required
def payment_success(request):
    """
    Handle the successful payment response from Stripe, update the user's subscription,
    and send a confirmation email including order details.
    """
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()  # Get all cart items before clearing them

    # Construct the order details for the email
    order_details = "Here is your order summary:\n\n"
    for item in cart_items:
        if item.product:
            order_details += f"- {item.product.name} (x{item.quantity}) - €{item.total_price()}\n"  # ✅ FIXED
        elif item.subscription:
            order_details += f"- {item.subscription.name} (Subscription) - €{item.subscription.price}\n"

    order_total = cart.get_total_cost() 
    order_details += f"\nTotal Amount: €{order_total}\n"

    # Clear the cart after successful payment
    cart.items.all().delete()

   # Handle subscriptions if applicable
    subscription_plan_id = request.session.get("selected_plan_id")
    if subscription_plan_id:
        plan = get_object_or_404(SubscriptionPlan, id=subscription_plan_id)
        user_profile = get_object_or_404(UserProfile, user=request.user)  # ✅ Corrected

        user_profile.subscription_plan = plan
        user_profile.subscription_start_date = timezone.now()
        user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=plan.duration)
        user_profile.save()

        messages.success(request, f"Successfully subscribed to the {plan.name} plan!")
        del request.session["selected_plan_id"]

        # Add subscription details to email
        order_details += f"\nYour subscription is valid until {user_profile.subscription_end_date.strftime('%Y-%m-%d')}."

    # Send confirmation email
    send_mail(
        subject="Order Confirmation - Rockfit",
        message=(
            f"Dear {request.user.username},\n\n"
            "Thank you for your purchase!\n\n"
            f"{order_details}\n\n"
            "Enjoy your order!\nRockfit Team"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    return render(request, "cart/payment_success.html", {"order_total": order_total})

@login_required
def payment_failed(request):
    user_email = request.user.email  

    send_mail(
        subject="Payment Failed - Rockfit",
        message="Unfortunately, your payment was unsuccessful. Please check your payment details and try again.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )

    messages.error(request, "Payment failed. Please check your details and try again.")
    return render(request, "cart/payment_failed.html")

'''
def cancel_view(request):
    """
    Handle the canceled payment response from Stripe.
    """
    return render(request, "cart/payment_cancel.html")


def add_subscription_to_cart(request, plan_id):
    """
    Add a subscription plan to the user's cart.
    Prevent adding more than one subscription.
    """
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    existing_subscription = CartItem.objects.filter(cart=cart, subscription__isnull=False).exists()
    if existing_subscription:
        messages.error(request, "You can only have one subscription in your cart.")
        return redirect("cart:view_cart") 

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, subscription=plan
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{plan.name} has been added to your cart!")
    return redirect("cart:view_cart")
