from django.urls import path
from .views import (
    home, 
    products, 
    product_detail, 
    subscription, 
    wishlist, 
    community_updates, 
    post_update, 
    update_profile
)

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('products/', products, name='products'),  # Products list page
    path('product/<int:pk>/', product_detail, name='product_detail'),  # Product detail page
    path('subscription/', subscription, name='subscription'),  # Subscription page
    path('wishlist/', wishlist, name='wishlist'),  # Wishlist page
    path('community-updates/', community_updates, name='community_updates'),  # Community updates page
    path('post-update/', post_update, name='post_update'),  # Page to post updates
    path('update-profile/', update_profile, name='update_profile'),  # User profile update page
]
