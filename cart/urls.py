"""
URL configuration for the cart application.

This module defines the URL patterns for cart-related views, including adding products to 
the cart, viewing the cart, removing or updating cart items, and handling the checkout and payment process.
"""
from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart, update_cart_item
from .views import create_checkout_session, payment_success, payment_cancel
from . import views

app_name = 'cart'  

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('', view_cart, name='view_cart'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
]
