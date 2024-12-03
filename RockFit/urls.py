"""
URL configuration for the main project.

This module defines the top-level URL patterns that direct HTTP requests to the appropriate 
applications within the project. It includes routes for the admin interface, fitness app, 
cart functionality, and user authentication using Django Allauth.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fitness.urls')),  # Include fitness app URLs
    path('cart/', include('cart.urls', namespace='cart')),  # Include cart app URLs
    path('accounts/', include('allauth.urls')),  # Include allauth's URLs
    #path('wishlist/', include('fitness.urls')),
]
