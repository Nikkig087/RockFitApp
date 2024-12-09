"""
Views for the cart application.

This module contains the views that handle cart functionality,
including viewing the cart, adding items to the cart, removing items,
updating quantities, and handling checkout and payments.
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from fitness.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from decimal import Decimal


@login_required
def view_cart(request):
    """
    Display the user's cart with all cart items and the total cost,
    including delivery fee.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()

        if not cart_items:
            messages.info(request, "Your cart is currently empty.")
            return render(
                request,
                "cart/cart.html",
                {
                    "cart_items": cart_items,
                    "total_cost": 0,
                    "delivery_fee": 0,
                    "final_total": 0,
                },
            )
        total_cost = cart.get_total_cost()

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
    else:
        return redirect("login")


def add_to_cart(request, product_id):
    """
    Add a product to the user's cart.

    Adds the specified product (by ID) to the cart of the authenticated user.
    If the product is already in the cart, its quantity is incremented.
    If the user is unauthenticated, the cart is stored in the session.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponse: Redirects to the 'product_list' page after adding
        the product to the cart.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
            cart_item.save()
        messages.success(
            request, f"{product.name} has been added to your cart!"
        )
    else:
        cart = request.session.get("cart", {})
        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Item added to your cart!")
    return redirect("product_list")


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

    line_items = []
    total_cost = 0
    for item in cart.items.all():
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
    if total_cost >= 50.00:
        delivery_fee = 0
    else:
        delivery_fee = 5.00
    if delivery_fee > 0:
        line_items.append(
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Delivery Fee",
                    },
                    "unit_amount": int(delivery_fee * 100),
                },
                "quantity": 1,
            }
        )
    if not line_items:
        return redirect("cart:view_cart")
    try:
        # Use reverse to resolve the URLs dynamically
        success_url = request.build_absolute_uri(reverse("cart:success"))
        cancel_url = request.build_absolute_uri(reverse("cart:cancel"))


        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return redirect(checkout_session.url)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")



def payment_success(request):
    """
    Handle the successful payment response from Stripe.

    This view is triggered after a successful payment and
    clears the user's cart by deleting all cart items.
    It then displays a success message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'payment_success.html' template.
    """
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    return render(request, "cart/payment_success.html")



    """
    Handle the canceled payment response from Stripe.

    This view is triggered when the user cancels the payment.
    It renders a cancelation message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'payment_cancel.html' template.
    """
def cancel_view(request):
    return render(request, 'cart/payment_cancel.html')
