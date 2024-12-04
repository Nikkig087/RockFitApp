"""
Views for the cart application.

This module contains the views that handle cart functionality, including viewing the cart, 
adding items to the cart, removing items, updating quantities, and handling checkout and payments.
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


def view_cart(request):
    """
    Display the user's cart with all cart items and the total cost.

    Retrieves the cart for the authenticated user, including all items and the total cost.
    If the user is not authenticated, redirects to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'cart/cart.html' template with the cart items and total cost.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_cost = cart.get_total_cost()
        return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('login') 

def add_to_cart(request, product_id):
    """
    Add a product to the user's cart.

    Adds the specified product (by ID) to the cart of the authenticated user. If the product 
    is already in the cart, its quantity is incremented. If the user is unauthenticated, 
    the cart is stored in the session.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponse: Redirects to the 'product_list' page after adding the product to the cart.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Get or create a cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # If item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
        else:
            # New item, set quantity to 1
            cart_item.quantity = 1
            cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart!")

    else:
        # For unauthenticated users, continue using session
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item added to your cart!")

    return redirect('product_list')  

@login_required
def remove_from_cart(request, cart_item_id):
    """
    Remove an item from the user's cart.

    Deletes the specified cart item from the user's cart. The cart item is identified by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_item_id (int): The ID of the cart item to be removed.

    Returns:
        HttpResponse: Redirects to the cart view after removal.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart!")
    return redirect('cart:view_cart')

@login_required
def update_cart_item(request, cart_item_id):
    """
    Update the quantity of an item in the user's cart.

    Handles POST requests to update the quantity of a specified cart item. The new quantity 
    is provided in the POST data.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_item_id (int): The ID of the cart item to update.

    Returns:
        HttpResponse: Redirects to the cart view after updating the item.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "Items updated in your cart!")
    return redirect('cart:view_cart')

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    """
    Create a Stripe checkout session for the user.

    This function prepares the line items based on the user's cart and initiates the checkout 
    session using the Stripe API. The user is redirected to the Stripe checkout page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the Stripe checkout URL.
    """
    cart = Cart.objects.get(user=request.user)
    line_items = []
    for item in cart.items.all():
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),  # Stripe expects cents
            },
            'quantity': item.quantity,
        })
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('cart:payment_success')),
        cancel_url=request.build_absolute_uri(reverse('cart:payment_cancel')),

    )
    return redirect(checkout_session.url)


def payment_success(request):
    """
    Handle the successful payment response from Stripe.

    This view is triggered after a successful payment and clears the user's cart by 
    deleting all cart items. It then displays a success message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'payment_success.html' template.
    """
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    return render(request, 'cart/payment_success.html')

def payment_cancel(request):
    """
    Handle the canceled payment response from Stripe.

    This view is triggered when the user cancels the payment. It renders a cancelation 
    message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'payment_cancel.html' template.
    """
    return render(request, 'cart/payment_cancel.html')

