<<<<<<< HEAD
from django.urls import path
=======
"""
URL configuration for the cart application.

This module defines the URL patterns for cart-related views,
including adding products to the cart, viewing the cart, removing or
updating cart items, and handling the checkout and payment process.
"""

from django.urls import path
from .views import (
    add_to_cart,
    view_cart,
    remove_from_cart,
    update_cart_item,
    add_subscription_to_cart,
)
from .views import (
    create_checkout_session,
    payment_success,
    cancel_view,
)
>>>>>>> 67b3728577e46b4c4146ea7bcfb871fd555ed2a0
from . import views

app_name = "cart"

urlpatterns = [
<<<<<<< HEAD
    path('add/<int:item_id>/<str:item_type>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('subscription/add_to_cart/<int:plan_id>/', views.add_subscription_to_cart, name='add_subscription_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/<int:order_id>/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('process_payment/', views.process_payment, name='process_payment'),
   
=======
    path(
        "add/<int:item_id>/<str:item_type>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path("", view_cart, name="view_cart"),
    path(
        "subscription/add_to_cart/<int:plan_id>/",
        views.add_subscription_to_cart,
        name="add_subscription_to_cart",
    ),
    path(
        "remove/<int:cart_item_id>/",
        remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "update/<int:cart_item_id>/",
        update_cart_item,
        name="update_cart_item",
    ),
    path("checkout/", views.create_checkout_session, name="checkout"),
    path("success/", views.payment_success, name="success"), #was just success
    path("cancel/", views.cancel_view, name="cancel"),
   # path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
       path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
>>>>>>> 67b3728577e46b4c4146ea7bcfb871fd555ed2a0
]
