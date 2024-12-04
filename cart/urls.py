"""
URL configuration for the cart application.

This module defines the URL patterns for cart-related views, including adding products to 
the cart, viewing the cart, removing or updating cart items, and handling the checkout and payment process.
"""
from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart, update_cart_item
from .views import create_checkout_session, payment_success, payment_cancel

app_name = 'cart'  # Use this namespace to avoid conflicts with other apps

urlpatterns = [
    # Route for adding a product to the cart
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),

    # Route for viewing the cart
    path('', view_cart, name='view_cart'),  # Cart view

    # Route for removing a product from the cart
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),

    # Route for updating the quantity of a cart item
    path('update/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),

    # Route for initiating the checkout process
    path('checkout/', create_checkout_session, name='checkout'),

    # Route for handling a successful payment
    path('payment-success/', payment_success, name='payment_success'),

    # Route for handling a canceled payment
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
]
