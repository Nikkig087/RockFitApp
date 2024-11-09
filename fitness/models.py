from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms

# Extending the User model with profile details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    name = models.CharField(max_length=100, blank=True)  # Add name field
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True)  # Add email field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    fitness_goal = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True) 
    phone = models.CharField(max_length=15, blank=True, null=True) 
    subscription_status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')
    subscription_plan = models.ForeignKey('SubscriptionPlan', on_delete=models.SET_NULL, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.user.username

# Subscription Plan model
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    benefits = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name

# Exercise Plan model
class ExercisePlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title

# Nutrition Plan model
class NutritionPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    diet_type = models.CharField(max_length=100)  
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    calories = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.title

# Product model for merchandise and nutrition products
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return self.name

# Order model for purchases
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
 
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# Review model for plans and products
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.product.id)])

# Community Update model
class CommunityUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Update by {self.user.username}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


