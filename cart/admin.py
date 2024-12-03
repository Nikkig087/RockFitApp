"""
Admin configuration for the cart application.

This module defines the admin interfaces for managing Cart and CartItem models 
in the Django admin site. It specifies how these models are displayed and listed.
"""
from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

