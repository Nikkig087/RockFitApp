"""
Context processors for providing cart and wishlist item counts.

These functions add cart and wishlist counts to the template context, 
allowing them to be displayed across all templates in a Django application.
"""
from cart.models import Cart
from .models import Wishlist

def cart_count(request):
 """
    Adds the total number of items in the user's cart to the template context.

    This context processor checks if the user is authenticated, then retrieves 
    the user's cart and counts the total number of items. If the cart does not 
    exist, the count is set to zero.

    Args:
        request (HttpRequest): The HTTP request object containing user information.

    Returns:
        dict: A dictionary containing the cart count with the key 'cart_count'.
"""
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_total_items()
        except Cart.DoesNotExist:
            count = 0
    return {'cart_count': count}

def wishlist_count(request):
 """
    Adds the total number of items in the user's wishlist to the template context.

    This context processor checks if the user is authenticated, then retrieves 
    or creates the user's wishlist and counts the total number of items. If the 
    user is not authenticated, the count is set to zero.

    Args:
        request (HttpRequest): The HTTP request object containing user information.

    Returns:
        dict: A dictionary containing the wishlist count with the key 'wishlist_count'.
    """
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        count = wishlist.items.count()  
    else:
        count = 0
    return {'wishlist_count': count}
