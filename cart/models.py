from django.db import models
from django.contrib.auth.models import User
from fitness.models import Product, SubscriptionPlan
from django.utils import timezone

class Cart(models.Model):
    """
    Represents a user's shopping cart.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_items(self):
        """Returns the total number of items in the cart."""
        return sum(item.quantity for item in self.items.all())

    def get_total_cost(self):
        """Returns the total cost of all items in the cart."""
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        """Returns the cost of this cart item."""
        if self.product:
            return self.product.price * self.quantity
        elif self.subscription:
            return self.subscription.price * self.quantity
        return 0

class FailedPayment(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_orders')
    order_date = models.DateTimeField(default=timezone.now)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)  # Add final_total
    status = models.CharField(max_length=20, default='pending')  # Add status
    full_name = models.CharField(max_length=255)  # Add full_name
    email = models.EmailField()  # Add email

    def get_total_cost(self):
        """Returns the total cost of all order items."""
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    """
    Represents an item in an order.
    """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        """Returns the cost of this order item."""
        if self.product:
            return self.product.price * self.quantity
        elif self.subscription:
            return self.subscription.price * self.quantity
        return 0

    def __str__(self):
        return f"Item in Order {self.order.id}"
