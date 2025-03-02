from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Order, OrderItem
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
from django.utils import timezone
import json
from django.template.loader import render_to_string
from django.http import HttpResponseServerError
import logging
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY 

@login_required

def payment_success(request):
    try:
        
        session_cart = request.session.get("cart_items", [])
        order_details = "Here is your order summary:\n\n"
        total_cost = 0

        
        for item in session_cart:
            price = Decimal(item['price'])  
            order_details += f"- {item['name']} (x{item['quantity']}) - €{price * item['quantity']}\n"
            total_cost += price * item['quantity']

        order_details += f"\nTotal Amount: €{total_cost}\n"

        
        request.session["cart_items"] = []
        request.session.modified = True

        
        subscription_plan_id = request.session.get("selected_plan_id")
        if subscription_plan_id:
            plan = get_object_or_404(SubscriptionPlan, id=subscription_plan_id)
            user_profile = get_object_or_404(UserProfile, user=request.user)

            user_profile.subscription_plan = plan
            user_profile.subscription_start_date = timezone.now()
            user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=plan.duration)
            user_profile.save()

            
            del request.session["selected_plan_id"]

           
            order_details += f"\nYour subscription is valid until {user_profile.subscription_end_date.strftime('%Y-%m-%d')}."
        
        # Return a rendered success page
        return render(request, "cart/success.html", {"total_cost": total_cost})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return HttpResponseServerError(f"An error occurred: {str(e)}")

# Checkout Page
from django.shortcuts import render, get_object_or_404
from .models import Order
def checkout(request, order_id):
    """
    Display the checkout page where the user can proceed with payment.
    """
    order = get_object_or_404(Order, id=order_id)

    # Pass the order and Stripe publishable key to the template
    context = {
        'order': order,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,  # Add the Stripe key here
    }
    
    return render(request, 'cart/checkout.html', context)



# Initialize logger
logger = logging.getLogger(__name__)


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




# views.py
from .models import Order, OrderItem, CartItem, Cart
from django.core.mail import send_mail

from django.http import JsonResponse
from .models import Order, OrderItem, Cart, CartItem
import stripe




'''
last cmted out 1212 2702
@login_required(login_url="login")
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

                # Send product email
                print("DEBUG - Sending product email")
                send_product_email(request.user, cart_item.product)

            elif cart_item.subscription:
                OrderItem.objects.create(
                    order=order,
                    subscription=cart_item.subscription,
                    quantity=cart_item.quantity
                )

        # Update user profile with subscription if any
        for cart_item in cart.items.all():
            if cart_item.subscription:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.subscription_plan = cart_item.subscription
                user_profile.subscription_start_date = timezone.now()
                user_profile.is_active = True
                user_profile.save()

                # Send subscription email
                print("DEBUG - Sending subscription email")
                send_subscription_email(request.user, cart_item.subscription)

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

def send_subscription_email(user, plan):
    subject = 'Subscription Confirmation'
    message = f'Thank you for subscribing to {plan.name}. Your subscription is now active.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    print(f"DEBUG - Subscription Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)

def send_product_email(user, product):
    subject = 'Product Purchase Confirmation'
    message = f'Thank you for purchasing {product.name}. We hope you enjoy your product!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    print(f"DEBUG - Product Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)

def send_failed_email(email, error_message):
    subject = 'Payment Failed'
    message = f'There was an error processing your payment: {error_message}. Please try again.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    print(f"DEBUG - Failed Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)
'''


'''
cmtd 2702 1452
@login_required(login_url="login")
def process_payment(request):
    data = json.loads(request.body)
    payment_method_id = data.get("payment_method_id")
    email = data.get("email")
    full_name = data.get("full_name")

    try:
        # Get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)

        # Calculate final total including delivery fee
        total_cost = sum(item.get_cost() for item in cart.items.all())
        delivery_fee = Decimal("5.00") if total_cost < Decimal("50.00") else Decimal("0.00")
        final_total = total_cost + delivery_fee

        # Create the order
        order = Order.objects.create(
            user=request.user,
            final_total=final_total,  # Use final total
            status='pending',
            full_name=full_name,
            email=email
        )

        # Create the order items
        for cart_item in cart.items.all():
            print(f"DEBUG - Cart Item: {cart_item}")
            print(f"DEBUG - Product: {cart_item.product} (Type: {type(cart_item.product)})")

            if cart_item.product:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

                # Send product email
                print("DEBUG - Sending product email")
                send_product_email(request.user, cart_item.product, final_total)

            elif cart_item.subscription:
                OrderItem.objects.create(
                    order=order,
                    subscription=cart_item.subscription,
                    quantity=cart_item.quantity
                )

                # Update user profile with subscription if any
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.subscription_plan = cart_item.subscription
                user_profile.subscription_start_date = timezone.now()
                user_profile.is_active = True
                user_profile.save()

                # Send subscription email
                print("DEBUG - Sending subscription email")
                send_subscription_email(request.user, cart_item.subscription, final_total)

        # Create Stripe PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.final_total * 100),  # Convert to cents
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
        return redirect('cart:payment_failed')

    except Exception as e:
        send_failed_email(email, str(e))
        return JsonResponse({"status": "failed", "error": str(e)})
        return redirect('cart:payment_failed')

def send_subscription_email(user, plan, final_total):
    subject = 'Subscription Confirmation'
    message = f' Dear {user}, thank you for subscribing to {plan.name}. Your subscription is now active.\nFinal Total: €{final_total}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    print(f"DEBUG - Subscription Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)
    
def send_product_email(user, product, final_total):
    subject = 'Product Purchase Confirmation'
    message = f'Dear {user},thank you for purchasing {product.name}. We hope you enjoy your product!\nFinal Total: €{final_total}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    print(f"DEBUG - Product Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)

def send_failed_email(email, error_message):
    subject = 'Payment Failed'
    message = f'Sorry there was an error processing your payment: {error_message}. Please try again.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    print(f"DEBUG - Failed Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)
'''

@login_required(login_url="login")
def process_payment(request):
    data = json.loads(request.body)
    payment_method_id = data.get("payment_method_id")
    full_name = data.get("full_name")
    address_1 = data.get("address_1", "")
    address_2 = data.get("address_2", "")
    city = data.get("city", "")

    try:
        # Get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)
        
        # Separate products and subscriptions
        products = []  # List to store product details for email
        subscription = None  # Store subscription details if any

        total_product_cost = 0  # To calculate the total product cost
        total_subscription_cost = 0  # To calculate the total subscription cost
        
        for cart_item in cart.items.all():
            if cart_item.product:
                total_product_cost += cart_item.product.price * cart_item.quantity
                products.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'total': cart_item.product.price * cart_item.quantity
                })
            elif cart_item.subscription:
                total_subscription_cost += cart_item.subscription.price * cart_item.quantity
                subscription = {
                    'plan': cart_item.subscription,
                    'quantity': cart_item.quantity,
                    'total': cart_item.subscription.price * cart_item.quantity
                }
                
                # Add subscription to user profile
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.subscription_plan = cart_item.subscription
                user_profile.subscription_start_date = timezone.now()
                user_profile.is_active = True
                user_profile.save()

        # Calculate the delivery fee for products only (if the product cost is less than €50)
        delivery_fee = Decimal("5.00") if total_product_cost < Decimal("50.00") else Decimal("0.00")
        final_product_total = total_product_cost + delivery_fee
        
        # Final totals
        final_subscription_total = total_subscription_cost  # No delivery fee for subscriptions
        final_total = final_product_total + final_subscription_total  # Sum of products and subscription totals
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            final_total=final_total,  # Use final total for order
            status='pending',
            full_name=full_name,
            email=request.user.email,
            address_line1=address_1,
            address_line2=address_2,
            city=city,
        )
        
        # Create order items for products
        for cart_item in cart.items.all():
            if cart_item.product:
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

        # Handle payment intent creation and confirmation
        payment_intent = stripe.PaymentIntent.create(
            amount=int(final_total * 100),  # Convert to cents
            currency="eur",
            payment_method=payment_method_id,
            confirmation_method="manual",
            confirm=True,
            return_url=request.build_absolute_uri(reverse("cart:success"))
        )

        if payment_intent.status != "succeeded":
            # PaymentIntent not succeeded, confirm it
            payment_intent = stripe.PaymentIntent.confirm(payment_intent.id)

        if payment_intent.status == "succeeded":
            # Payment successful, send the emails
            if products:
                send_product_email(request.user, products, final_product_total, delivery_fee)  # Send email with delivery fee for products

            if subscription:
                send_subscription_email(request.user, subscription, final_subscription_total)  # Send separate email for subscription

            # Clear the cart after payment and email sending
            cart.items.all().delete()

            # Return a success response
            return JsonResponse({"status": "success", "client_secret": payment_intent.client_secret})
        else:
            # Payment failed, handle failure
            send_failed_email(request.user, "Payment not succeeded")
            return redirect('cart:payment_failed')

    except stripe.error.CardError as e:
        send_failed_email(request.user, str(e))
        return redirect('cart:payment_failed')
    except Exception as e:
        send_failed_email(request.user, str(e))
        return redirect('cart:payment_failed')



def send_subscription_email(user, subscription, final_subscription_total):
    print(f"DEBUG - Type of subscription: {type(subscription)}")

    try:
        subscription_plan = subscription['plan']  # Extract subscription plan from dict

        if not subscription_plan:
            print("Error: Subscription plan not found.")
            return

        # Prepare the email for the subscription
        subject = 'Subscription Confirmation - Rockfit'
        message = f"Dear {user.username},\n\nThank you for subscribing to the {subscription_plan.name} plan. Your subscription is now active.\n\n" \
                  f"Quantity: {subscription['quantity']}\nTotal Cost for Subscription: €{subscription['total']}\n\n" \
                  f"Final Subscription Total: €{final_subscription_total}\n\n"

        # Add Subscription Info from UserProfile (Only if there's a subscription)
        user_profile, created = UserProfile.objects.get_or_create(user=user)  # Ensure we have the UserProfile
        if user_profile.subscription_plan:
            # Ensure start and end dates are not None before using strftime
            subscription_details = (
                f"\n📅 **Subscription Details:**\n"
                f"Plan: {user_profile.subscription_plan.name}\n"
                f"Price: €{user_profile.subscription_plan.price}\n"
                f"Duration: {user_profile.subscription_plan.duration} days\n"
                f"Start Date: {user_profile.subscription_start_date.strftime('%Y-%m-%d') if user_profile.subscription_start_date else 'Not Available'}\n"
                f"End Date: {user_profile.subscription_end_date.strftime('%Y-%m-%d') if user_profile.subscription_end_date else 'Not Available'}\n"
            )
            message += subscription_details  # Append subscription details to the message

        # Finish the email body
        message += "\nEnjoy your subscription!\nRockfit Team"

        # Define the sender and recipient email
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        # Debug print for checking email content
        print(f"DEBUG - Subscription Email: {subject}, {message}, {from_email}, {recipient_list}")
        
        # Send the email
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    except Exception as e:
        print(f"Error sending subscription email: {e}")


def send_product_email(user, products, final_product_total, delivery_fee):
    # Build a product list to include in the email message
    product_details = "\n".join([f"Product: {product['product'].name}, Quantity: {product['quantity']}, Total: €{product['total']}" for product in products])
    
    subject = 'Product Purchase Confirmation'
    message = f"Dear {user.username},\n\nThank you for purchasing the following products:\n\n" \
              f"{product_details}\n\nFinal Total for Products: €{final_product_total}\n" \
              f"Delivery Fee: €{delivery_fee}\n\nWe hope you enjoy your products!\n\nRockfit Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    print(f"DEBUG - Product Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)


def send_failed_email(user, error_message):
    subject = 'Payment Failed'
    message = f"Dear {user.username}, \n\n" \
              f"There was an error processing your payment: {error_message}.\n\n" \
              f" Please try again."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    print(f"DEBUG - Failed Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)




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



'''
cmted 1105 2702
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

    # Retrieve the pending order for the logged-in user, create if it doesn't exist
    order, created = Order.objects.get_or_create(user=request.user, status="pending", defaults={'total_price': final_total})

    # If the order was retrieved (not created) update the total_price
    if not created:
        order.total_price = final_total
        order.save()

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
'''

'''
last cmted out 1212 2702
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

    # Retrieve or create the first pending order for the logged-in user
    orders = Order.objects.filter(user=request.user, status="pending")
    if orders.exists():
        order = orders.first()
        # Delete any additional pending orders
        orders.exclude(id=order.id).delete()
    else:
        order = Order(user=request.user, status="pending", total_price=final_total)
        order.save()
    
    order.total_price = final_total
    order.save()

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
'''
@login_required(login_url="login")
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    # Calculate the total cost and delivery fee as needed
    total_cost = sum(item.get_cost() for item in cart_items)

    delivery_fee = Decimal("5.00") if total_cost < Decimal("50.00") else Decimal("0.00")
    final_total = total_cost + delivery_fee

    # Retrieve or create the first pending order for the logged-in user
    orders = Order.objects.filter(user=request.user, status="pending")
    if orders.exists():
        order = orders.first()
        # Delete any additional pending orders
        orders.exclude(id=order.id).delete()
    else:
        order = Order(user=request.user, status="pending", final_total=final_total)
        order.save()
    
    order.final_total = final_total
    order.save()

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




@login_required
def add_to_cart(request, item_id, item_type):
    from fitness.models import Product, SubscriptionPlan  # Ensure import

    if item_type == "product":
        item = get_object_or_404(Product, id=item_id)
    elif item_type == "subscription":
        item = get_object_or_404(SubscriptionPlan, id=item_id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect("fitness:products")

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        if item_type == "product":
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item)
            if not created:
                cart_item.quantity += 1
            cart_item.save()
        
        # Store item details in session for email
        session_cart = request.session.get("cart_items", [])
        session_cart.append({
            "name": item.name,
            "quantity": cart_item.quantity,
            "price": str(item.price)  # Convert price to string
        })
        request.session["cart_items"] = session_cart
        request.session.modified = True

        
    else:
        # Handle unauthenticated users (similar logic for session storage)
        cart = request.session.get("cart", {})
        key = f"{item_type}_{item_id}"
        if key in cart:
            cart[key]["quantity"] += 1
        else:
            cart[key] = {"type": item_type, "quantity": 1}
        request.session["cart"] = cart
        request.session.modified = True
       

    return redirect("fitness:products")
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
   # messages.success(request, "Item removed from your cart!")
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
'''
''
@login_required
def payment_failed(request):
    user_email = request.user.email  
    '''
    send_mail(
        subject="Payment Failed - Rockfit",
        message="Unfortunately, your payment was unsuccessful. Please check your payment details and try again.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
    '''
   
    return render(request, "cart/payment_failed.html")

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