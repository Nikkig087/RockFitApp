from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Order, OrderItem

from fitness.models import Product, SubscriptionPlan, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import json
from django.template.loader import render_to_string
from django.http import HttpResponseServerError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from decimal import Decimal


stripe.api_key = settings.STRIPE_SECRET_KEY 

@login_required

def payment_success(request):
    """
    Handle the successful payment response from Stripe and update the user's subscription.
    
    This view processes the cart items, generates an order summary, clears the cart, 
    updates the user's subscription plan if applicable, and displays a success message.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the success page with the total cost of the transaction.
    """
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
            
            user_profile.save()

            
            del request.session["selected_plan_id"]

           
            
        
        
        return render(request, "cart/success.html", {"total_cost": total_cost})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return HttpResponseServerError(f"An error occurred: {str(e)}")



def checkout(request, order_id):
    """
    Display the checkout page where the user can proceed with payment.
    """
    order = get_object_or_404(Order, id=order_id)

    
    context = {
        'order': order,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,  
    }
    
    return render(request, 'cart/checkout.html', context)



@login_required(login_url="login")
def process_payment(request):
    """
    Process the payment using Stripe and redirect accordingly.
    """
    data = json.loads(request.body)
    payment_method_id = data.get("payment_method_id")
    full_name = data.get("full_name")
    address_1 = data.get("address_1", "")
    address_2 = data.get("address_2", "")
    city = data.get("city", "")

    try:
        
        cart = Cart.objects.get(user=request.user)
        
        
        products = [] 
        subscription = None  

        total_product_cost = 0  
        total_subscription_cost = 0  
        
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
                
                
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.subscription_plan = cart_item.subscription
                user_profile.subscription_start_date = timezone.now()
                user_profile.is_active = True
                user_profile.save()

       
        delivery_fee = Decimal("5.00") if total_product_cost < Decimal("50.00") else Decimal("0.00")
        final_product_total = total_product_cost + delivery_fee
        
        
        final_subscription_total = total_subscription_cost  
        final_total = final_product_total + final_subscription_total  
        
        
        order = Order.objects.create(
            user=request.user,
            final_total=final_total,  
            status='pending',
            full_name=full_name,
            email=request.user.email,
            address_line1=address_1,
            address_line2=address_2,
            city=city,
        )
        
        
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

        
        payment_intent = stripe.PaymentIntent.create(
            amount=int(final_total * 100),  
            currency="eur",
            payment_method=payment_method_id,
            confirmation_method="manual",
            confirm=True,
            return_url=request.build_absolute_uri(reverse("cart:success"))
        )

        if payment_intent.status != "succeeded":
            
            payment_intent = stripe.PaymentIntent.confirm(payment_intent.id)

        if payment_intent.status == "succeeded":
            
            if products:
                send_product_email(request.user, products, final_product_total, delivery_fee)  

            if subscription:
                send_subscription_email(request.user, subscription, final_subscription_total)  

            
            cart.items.all().delete()

            
            return JsonResponse({"status": "success", "client_secret": payment_intent.client_secret})
        else:
            
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
    """
    Send a confirmation email to the user for a successful subscription purchase.
    
    Args:
        user (User): The user who purchased the subscription.
        subscription (dict): Information about the subscription plan.
        final_subscription_total (Decimal): Total cost of the subscription.
    """
    try:
        subscription_plan = subscription['plan']  

        if not subscription_plan:
            print("Error: Subscription plan not found.")
            return

        
        subject = 'Subscription Confirmation - Rockfit'
        message = f"Dear {user.username},\n\nThank you for subscribing to the {subscription_plan.name} plan. Your subscription is now active.\n\n" \
                  f"Quantity: {subscription['quantity']}\nTotal Cost for Subscription: €{subscription['total']}\n\n" \
                  f"Final Subscription Total: €{final_subscription_total}\n\n"

        
        user_profile, created = UserProfile.objects.get_or_create(user=user)  
        if user_profile.subscription_plan:
            
            subscription_details = (
                f"\n📅 **Subscription Details:**\n"
                f"Plan: {user_profile.subscription_plan.name}\n"
                f"Price: €{user_profile.subscription_plan.price}\n"
                f"Duration: {user_profile.subscription_plan.duration} days\n"
                f"Start Date: {user_profile.subscription_start_date.strftime('%Y-%m-%d') if user_profile.subscription_start_date else 'Not Available'}\n"
              
            )
            message += subscription_details  

        
        message += "\nEnjoy your subscription!\nRockfit Team"

       
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        
        print(f"DEBUG - Subscription Email: {subject}, {message}, {from_email}, {recipient_list}")
        
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    except Exception as e:
        print(f"Error sending subscription email: {e}")


def send_product_email(user, products, final_product_total, delivery_fee):
    """
    Send a confirmation email to the user for successful product purchase.
    
    Args:
        user (User): The user who made the purchase.
        products (list): List of products purchased.
        final_product_total (Decimal): Total cost of the products.
        delivery_fee (Decimal): Delivery fee for the products.
    """
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
    """
    Send an email to the user in case of a failed payment.

    Args:
        user (User): The user who attempted the payment.
        error_message (str): The error message explaining why the payment failed.
    """
    subject = 'Payment Failed'
    message = f"""
    <html>
        <body>
            <p>Dear {user.username},</p>
            <p style="color: red; font-size: 16px; font-weight: bold;">
                There was an error processing your payment: <strong>{error_message}</strong>.
            </p>
            <p>
                Please try again or feel free to reach out to us via our Contact Form on our website.
            </p>
            <p>
                Kind regards,<br>
                <strong>The Rockfit Team</strong>
            </p>
        </body>
    </html>
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    print(f"DEBUG - Failed Email: {subject}, {message}, {from_email}, {recipient_list}")
    send_mail(subject, message, from_email, recipient_list)


@login_required(login_url="login")
def view_cart(request):
    """
    Display the user's shopping cart and calculate the total cost, including delivery fees.

    This view fetches the user's cart, calculates the total cost of the items in the cart,
    and renders the cart page with all the necessary details.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the cart page with cart items and the total cost.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    
    total_cost = sum(item.get_cost() for item in cart_items)

    delivery_fee = Decimal("5.00") if total_cost < Decimal("50.00") else Decimal("0.00")
    final_total = total_cost + delivery_fee

    
    orders = Order.objects.filter(user=request.user, status="pending")
    if orders.exists():
        order = orders.first()
        
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
            "order": order,  
        },
    )


@login_required
def add_to_cart(request, item_id, item_type):
    from fitness.models import Product, SubscriptionPlan  

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
        
        
        session_cart = request.session.get("cart_items", [])
        session_cart.append({
            "name": item.name,
            "quantity": cart_item.quantity,
            "price": str(item.price)  
        })
        request.session["cart_items"] = session_cart
        request.session.modified = True

        
    else:
        
        cart = request.session.get("cart", {})
        key = f"{item_type}_{item_id}"
        if key in cart:
            cart[key]["quantity"] += 1
        else:
            cart[key] = {"type": item_type, "quantity": 1}
        request.session["cart"] = cart
        request.session.modified = True
       

    return redirect("fitness:products")


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


@login_required
def payment_failed(request):
    user_email = request.user.email  
    
   
    return render(request, "cart/payment_failed.html")

def cancel_view(request):
    """
    Handle the canceled payment request from User.
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
    
    return redirect("cart:view_cart")