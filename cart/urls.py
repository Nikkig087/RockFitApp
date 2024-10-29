# cart/urls.py

from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart, update_cart_item

app_name = 'cart'  # Use this namespace to avoid conflicts with other apps

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('', view_cart, name='view_cart'),  # Cart view
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
]
