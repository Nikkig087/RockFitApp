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
    """
    Represents an item in the shopping cart, which can either be a product or a subscription plan.

    Attributes:
        cart (ForeignKey): The cart that this item belongs to.
        product (ForeignKey, nullable): The product associated with this cart item.
        subscription (ForeignKey, nullable): The subscription plan associated with this cart item.
        quantity (PositiveIntegerField): The quantity of the item in the cart.

    Methods:
        get_cost(): Returns the cost of this cart item based on the product or subscription.
    """

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
    """
    Stores information about failed payments, including the user's email and the amount.
    
    Attributes:
        email (EmailField): The email address associated with the failed payment.
        amount (DecimalField): The amount of money associated with the failed payment.
        created_at (DateTimeField): The timestamp when the failed payment occurred.
    """
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    """
    Represents a user's order, which contains information about the products purchased, the total amount, 
    and the status of the order.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_orders')
    order_date = models.DateTimeField(default=timezone.now)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)  
    status = models.CharField(max_length=20, default='pending')  
    full_name = models.CharField(max_length=255)  
    email = models.EmailField()  

      
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

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
