from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms

# Extending the User model with profile details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    name = models.CharField(max_length=100, blank=True)  # Add name field
    email = models.EmailField(blank=True)  # Add email field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    fitness_goal = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)  # Optional field
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional field
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
    diet_type = models.CharField(max_length=100)  # e.g. Vegan, Keto
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    calories = models.CharField(max_length=100)  # e.g. 360kcal
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    exercise_plan = models.ForeignKey(ExercisePlan, null=True, blank=True, on_delete=models.CASCADE)
    nutrition_plan = models.ForeignKey(NutritionPlan, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f"Review by {self.user.username}"

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
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')  # Use a related name here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


