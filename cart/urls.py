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
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    """
    Route for adding a product to the cart.

    This URL maps to the 'add_to_cart' view, which adds the specified product 
    (identified by its product_id) to the user's cart.

    Args:
        product_id (int): The ID of the product to be added to the cart.

    Example:
        URL: 'cart/add/123/' will add the product with ID 123 to the cart.
    """
    path('', view_cart, name='view_cart'),  # Cart view
    """
    Route for viewing the cart.

    This URL maps to the 'view_cart' view, which displays all items in the user's cart.

    Example:
        URL: 'cart/' will show the current items in the cart.
    """
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    """
    Route for removing a product from the cart.

    This URL maps to the 'remove_from_cart' view, which removes the cart item specified 
    by the cart_item_id from the user's cart.

    Args:
        cart_item_id (int): The ID of the cart item to be removed.

    Example:
        URL: 'cart/remove/456/' will remove the cart item with ID 456.
    """
    path('update/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    """
    Route for updating the quantity of a cart item.

    This URL maps to the 'update_cart_item' view, which allows the user to update the 
    quantity of a specified cart item.

    Args:
        cart_item_id (int): The ID of the cart item to be updated.

    Example:
        URL: 'cart/update/789/' will update the quantity of the cart item with ID 789.
    """
    path('checkout/', create_checkout_session, name='checkout'),
    """
    Route for initiating the checkout process.

    This URL maps to the 'create_checkout_session' view, which starts the checkout 
    session, allowing users to proceed with their payment.

    Example:
        URL: 'cart/checkout/' will redirect the user to the checkout page.
    """
    path('payment-success/', payment_success, name='payment_success'),
    """
    Route for handling a successful payment.

    This URL maps to the 'payment_success' view, which is triggered after a successful 
    payment is made by the user.

    Example:
        URL: 'cart/payment-success/' will display a success message after a successful payment.
    """
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
    """
    Route for handling a canceled payment.

    This URL maps to the 'payment_cancel' view, which is triggered if the user cancels 
    the payment process.

    Example:
        URL: 'cart/payment-cancel/' will display a message indicating the payment was canceled.
    """

]
