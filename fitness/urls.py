"""
URL configuration for the fitness application.

This module defines URL patterns for various views in the fitness application, 
including home, products, subscriptions, community updates, wishlists, and user profiles. 
It maps URLs to their corresponding view functions or classes.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    home, 
    products, 
    product_detail, 
    community_updates,
    post_update, 
    
)
from .views import subscription_plans,subscribe, profile_view, update_profile#, subscription_viewnames

from .views import (
    add_to_wishlist,
    view_wishlist,
    remove_from_wishlist,
    wishlist_count
)

urlpatterns = [
    path('', views.home, name='home'),  # Home page as root
    path('products/', products, name='products'),  # Products list page
    path('product_list/', products, name='product_list'),  # product-list URL
    path('product/<int:product_id>/', product_detail, name='product_detail'),  # Product detail page
    path('subscription/', subscription_plans, name='subscription'),
    path('subscription/subscribe/<int:plan_id>/', subscribe, name='subscribe'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('wishlist/', view_wishlist, name='view_wishlist'),  # Ensure this name is correct
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
  
    path('community-updates/', community_updates, name='community_updates'),  # Community updates page
    path('post-update/', post_update, name='post_update'),  # Page to post updates
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('profile/', views.profile_view, name='profile'),  # Profile page
    path('update-profile/', views.update_profile, name='update_profile'),



    path('product/<int:product_id>/review/create/', views.create_review, name='create_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    
    path('subscription/', views.subscription_plans, name='subscription'),  # Correct URL
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),  # Subscribe to a plan
]