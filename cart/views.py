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


@login_required(login_url="login")
def view_cart(request):
    """
    Display the user's cart with all cart items and the total cost.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_cost = sum(
        (item.product.price if item.product else item.subscription.price)
        * item.quantity
        for item in cart_items
    )

    if total_cost >= Decimal("50.00"):
        delivery_fee = Decimal("0.00")
    else:
        delivery_fee = Decimal("5.00")
    final_total = total_cost + delivery_fee

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "total_cost": total_cost,
            "delivery_fee": delivery_fee,
            "final_total": final_total,
        },
    )


def add_to_cart(request, item_id, item_type):
    """
    Add a product or subscription to the user's cart.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the product or subscription.
        item_type (str): Either "product" or "subscription".

    Returns:
        HttpResponse: Redirects to the appropriate page.
    """
    if item_type == "product":
        item = get_object_or_404(Product, id=item_id)
    elif item_type == "subscription":
        return add_subscription_to_cart(request, item_id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect("fitness:products")  # Corrected the URL name here
    
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


def process_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        payment_intent_id = request.session.get("payment_intent_id")

        if not payment_intent_id:
            messages.error(request, "Payment session expired. Please try again.")
            return redirect("cart:cart_view")

        
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        logger.info(f" Payment Intent Status: {payment_intent.status}")

        if payment_intent.status == "succeeded":
            return redirect("cart:payment_success")

        elif payment_intent.status in ["requires_payment_method", "requires_action", "canceled"]:
            logger.error("Payment failed: Insufficient funds or card declined!")

            
            send_mail(
                subject="Payment Failed - Rockfit",
                message="Your payment was unsuccessful. Please check your card details and try again.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            return redirect("cart:payment_failed")

        else:
            logger.error(f"Unexpected payment status: {payment_intent.status}")
            messages.error(request, "An unexpected payment issue occurred. Please try again.")
            return redirect("cart:payment_failed")

    except stripe.error.CardError as e:
        logger.error(f"Stripe CardError: {e.user_message}")
        messages.error(request, f"Your card was declined: {e.user_message}")

        send_mail(
            subject="Payment Failed - Rockfit",
            message=f"Dear {request.user.username},\n\nYour payment was unsuccessful. Reason: {e.user_message}. "
                    "Please check your payment details and try again.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        return redirect("cart:payment_failed")

    except Exception as e:
        logger.error(f"🚨 Unexpected error: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("cart:payment_failed")

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



def create_checkout_session(request):
    cart = get_object_or_404(Cart, user=request.user)

    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:view_cart")  

    line_items = []
    for item in cart.items.all():
        price = item.product.price if item.product else item.subscription.price
        line_items.append(
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": item.product.name if item.product else item.subscription.name},
                    "unit_amount": int(price * 100),
                },
                "quantity": item.quantity if item.product else 1,
            }
        )

    try:
        success_url = request.build_absolute_uri(reverse("cart:success"))
        cancel_url = request.build_absolute_uri(reverse("cart:cancel"))

        # No direct "failure_url" in Stripe Checkout, so we use metadata to track user
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=request.user.id,
            metadata={"user_email": request.user.email},  # Store user email in Stripe metadata
        )

        return redirect(checkout_session.url)

    except Exception as e:
        return render(request, "cart/payment_failed.html", {"error": str(e)})  # Show error directly in failed.html


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'status': 'invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session['payment_status'] == 'paid':
            # Handle successful payment here

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        user_email = session['customer_email']

        send_mail(
            subject="Payment Failed - Rockfit",
            message="Your payment was unsuccessful. Please check your card details and try again.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

    return JsonResponse({'status': 'success'})

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

'''

def payment_failed(request):
    """
    Handles failed payments by checking Stripe sessions and sending an email.
    """
    session_id = request.GET.get("session_id")

    if not session_id:
        return render(request, "cart/payment_failed.html", {"error": "No session ID provided."})

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        # Check if payment was not successful
        if session.payment_status == "unpaid":
            user_email = session.metadata.get("user_email")  

            # Send failure email
            send_mail(
                "Payment Failed - Rockfit",
                "Unfortunately, your payment was unsuccessful. Please try again.",
                "noreply@rockfit.com",
                [user_email],
            )

        return render(request, "cart/payment_failed.html")

    except Exception as e:
        return render(request, "cart/payment_failed.html", {"error": str(e)})
'

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
