
"""
Models for the cart application.

This module defines the models related to the shopping cart functionality,
including the Cart and CartItem models. These models represent the user's cart
and the items within it.
"""

from django.db import models
from django.contrib.auth.models import User
from fitness.models import Product, SubscriptionPlan


class Cart(models.Model):
    """
    Represents a user's shopping cart.

    The Cart model is associated with a single user, and it holds the user's
    selected products (via CartItem objects). It includes methods to calculate
    the total cost and the total number of items in the cart.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_cost(self):
        """
        Calculate the total cost of the cart, considering both products and subscriptions.
        """
        total_cost = 0
        for item in self.items.all():
            if item.product:
                total_cost += item.product.price * item.quantity
            elif item.subscription:
                total_cost += item.subscription.price * item.quantity
        return total_cost
    def get_total_items(self):
        """
        Calculate the total number of items in the cart.

        Returns:
            int: The total number of items in the cart.
        """
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Represents an item in a user's shopping cart.

    Attributes:
        cart (Cart): The cart the item belongs to.
        product (Product): The product being added to the cart.
        subscription (SubscriptionPlan): The subscription being
        added to the cart.
        quantity (int): The quantity of the product or
        subscription in the cart.
    """

    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        SubscriptionPlan, null=True, blank=True, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    def total_price(self):
        """Calculate the total price of this cart item."""
        if self.product:
            return self.product.price * self.quantity
        elif self.subscription:
            return self.subscription.price  # Subscriptions may not have quantities
        return 0 
    def __str__(self):
        """
        Return a string representation of the CartItem.
        """
        if self.product:
            return f"{self.product.name} (x{self.quantity})"
        elif self.subscription:
            return f"{self.subscription.name} (x{self.quantity})"
        return "CartItem"



class FailedPayment(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)