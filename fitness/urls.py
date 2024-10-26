from django.urls import path
from . import views
from .views import (
    home, 
    products, 
    product_detail, 
    wishlist, 
    community_updates, 
    post_update, 
    
)
from .views import subscription_plans,subscribe, profile_view, update_profile


urlpatterns = [
    path('', home, name='home'),  # Home page as root
    path('products/', products, name='products'),  # Products list page
    path('product-list/', products, name='product-list'),  # product-list URL
    path('product/<int:product_id>/', product_detail, name='product_detail'),  # Product detail page
     path('subscription/', subscription_plans, name='subscription'),
    path('subscription/subscribe/<int:plan_id>/', subscribe, name='subscribe'),
    path('wishlist/', wishlist, name='wishlist'),  # Wishlist page
    path('community-updates/', community_updates, name='community_updates'),  # Community updates page
    path('post-update/', post_update, name='post_update'),  # Page to post updates
     path('profile/', profile_view, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),  # Correct function name
   # path('subscription/', subscription_viewnames, name='subscription'),  # Assuming this is correct
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to Cart view

]
