from django.urls import path
from . import views

app_name = 'cart'  # Namespacing the app

urlpatterns = [
    path('', views.view_cart, name='view_cart'),  # Cart view
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),  # Update cart item
]


