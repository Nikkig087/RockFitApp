"""
Views for the cart application.

This module contains the views that handle cart functionality,
including viewing the cart, adding items to the cart, removing items,
updating quantities, and handling checkout and payments.
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from fitness.models import Product, SubscriptionPlan
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from decimal import Decimal


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
        HttpResponse: Redirects to the product list or subscription page.
    """
    if item_type == "product":
        item = get_object_or_404(Product, id=item_id)
    elif item_type == "subscription":
        item = get_object_or_404(SubscriptionPlan, id=item_id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect("product_list")
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        if item_type == "product":
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=item
            )
        elif item_type == "subscription":
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, subscription=item
            )
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
    return redirect(
        "product_list" if item_type == "product" else "subscription"
    )


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
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "Items updated in your cart!")
    return redirect("cart:view_cart")


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    """
    Create a Stripe checkout session with the user's cart items.
    """
    cart = get_object_or_404(Cart, user=request.user)

    subscription_plan = None

    line_items = []
    total_cost = 0

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
    if not line_items:
        return redirect("cart:view_cart")
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


@login_required
def payment_success(request):
    """
    Handle the successful payment response from Stripe and
    update the user's subscription.
    """

    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()

    subscription_plan_id = request.session.get("selected_plan_id")

    if subscription_plan_id:

        plan = get_object_or_404(SubscriptionPlan, id=subscription_plan_id)

        user_profile = request.user.userprofile
        user_profile.subscription_plan = plan
        user_profile.subscription_start_date = timezone.now()
        user_profile.subscription_end_date = (
            timezone.now() + timezone.timedelta(days=plan.duration)
        )
        user_profile.save()

        messages.success(
            request, f"Successfully subscribed to the {plan.name} plan!"
        )
        del request.session["selected_plan_id"]
    return render(request, "cart/payment_success.html")


def cancel_view(request):
    """
    Handle the canceled payment response from Stripe.

    This view is triggered when the user cancels the payment,
    and it renders a cancellation message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'payment_cancel.html' template.
    """
    return render(request, "cart/payment_cancel.html")


def add_subscription_to_cart(request, plan_id):
    """
    Add a subscription plan to the user's cart.
    """
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, subscription=plan
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{plan.name} has been added to your cart!")
    return redirect("cart:view_cart")
