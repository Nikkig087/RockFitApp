# cart/models.py

from django.db import models
from django.contrib.auth.models import User
from fitness.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_total_cost(self):
        # Use the related_name 'items' to access CartItem objects
        return sum(item.product.price * item.quantity for item in self.items.all())
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())  # Sum up the quantities of all CartItem instances

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"