"""
Models for the cart application.

This module defines the models related to the shopping cart functionality, including 
the Cart and CartItem models. These models represent the user's cart and the items within it.
"""
from django.db import models
from django.contrib.auth.models import User
from fitness.models import Product

class Cart(models.Model):
    """
    Represents a user's shopping cart.

    The Cart model is associated with a single user, and it holds the user's selected products 
    (via CartItem objects). It includes methods to calculate the total cost and the total 
    number of items in the cart.

    Attributes:
        user (User): The user associated with the cart.
        created_at (datetime): The date and time when the cart was created.

    Methods:
        get_total_cost(): Returns the total cost of all items in the cart.
        get_total_items(): Returns the total number of items (sum of quantities) in the cart.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_total_cost(self):
        """
        Calculate the total cost of all items in the cart.

        This method multiplies the price of each product by its quantity and sums the values 
        to get the total cost of the cart.

        Returns:
            float: The total cost of the cart.
        """
        # Use the related_name 'items' to access CartItem objects
        return sum(item.product.price * item.quantity for item in self.items.all())
    
    def get_total_items(self):
        """
        Calculate the total number of items in the cart.

        This method sums up the quantities of all CartItem instances associated with the cart.

        Returns:
            int: The total number of items in the cart.
        """
        return sum(item.quantity for item in self.items.all())  # Sum up the quantities of all CartItem instances

class CartItem(models.Model):
    """
    Represents an item in a user's shopping cart.

    The CartItem model links a Cart to a Product, and tracks the quantity of each product 
    that the user has added to the cart.

    Attributes:
        cart (Cart): The cart that the item belongs to.
        product (Product): The product being added to the cart.
        quantity (int): The quantity of the product in the cart.

    Methods:
        __str__(): Returns a string representation of the CartItem (product name and quantity).
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
          """
        Return a string representation of the CartItem.

        This method returns the product name and quantity in a human-readable format.

        Returns:
            str: A string representation of the CartItem, e.g., "ProductName (x2)".
        """
        return f"{self.product.name} (x{self.quantity})"