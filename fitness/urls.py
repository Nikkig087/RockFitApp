from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),

    path('products/', views.products, name='products'),
    path('product_list/', views.products, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscription/', views.subscription_view, name='subscription'),
    path('profile/', views.profile_view, name='profile'),
    path('pause-subscription/', views.request_pause_subscription, name='request_pause_subscription'),
    path('resume-subscription/', views.resume_subscription, name='resume_subscription'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('community-updates/', views.community_updates, name='community_updates'),
    path('post-update/', views.post_update, name='post_update'),
    path('contact/', views.contact_form, name='contact_form'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('product/<int:product_id>/review/create/', views.create_review, name='create_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    # Include allauth URLs for authentication
    path('accounts/', include('allauth.urls')),  # This includes login, signup, etc.
]