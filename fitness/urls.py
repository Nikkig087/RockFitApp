from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    home, 
    products, 
    product_detail, 
    wishlist, 
    community_updates, 
    post_update, 
    
)
from .views import subscription_plans,subscribe, profile_view, update_profile#, subscription_viewnames


urlpatterns = [
    path('', home, name='home'),  # Home page as root
    path('products/', products, name='products'),  # Products list page
    path('product-list/', products, name='product-list'),  # product-list URL
    path('product/<int:product_id>/', product_detail, name='product_detail'),  # Product detail page
     path('subscription/', subscription_plans, name='subscription'),
    path('subscription/subscribe/<int:plan_id>/', subscribe, name='subscribe'),
    path('wishlist/', views.wishlist, name='wishlist'),  # Wishlist page
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('community-updates/', community_updates, name='community_updates'),  # Community updates page
    path('post-update/', post_update, name='post_update'),  # Page to post updates
    path('profile/', views.profile_view, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('update-profile/', update_profile, name='update_profile'),  # Correct function name
  # path('subscription/', subscription_viewnames, name='subscription'),  
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to Cart view
     

]
