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
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_cost = cart.get_total_cost()
        return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('login') 

def add_to_cart(request, product_id):
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
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart!")
    return redirect('cart:view_cart')

@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "Items updated in your cart!")
    return redirect('cart:view_cart')

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
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
    # Clear the user's cart after successful payment
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    return render(request, 'cart/payment_success.html')

def payment_cancel(request):
    return render(request, 'cart/payment_cancel.html')

