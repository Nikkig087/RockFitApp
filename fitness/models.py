"""
Models for the fitness application.

This module defines the database models for various entities such as users, 
subscription plans, exercise plans, nutrition plans, products, orders, reviews, 
community updates, and wishlists. These models represent the structure of the 
application's data and include fields, relationships, and methods.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms

class SubscriptionPlan(models.Model):
    """
    Represents a subscription plan available for users.

    Attributes:
        name (str): The name of the subscription plan.
        price (Decimal): The price of the subscription plan.
        duration (int): The duration of the plan in days.
        benefits (str): A description of the plan's benefits.
        is_active (bool): Indicates if the plan is currently active.
        is_spotlight (bool): Highlights the plan as a featured option.
        created_at (datetime): The date and time when the plan was created.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # Duration in days
    benefits = models.TextField()
    is_active = models.BooleanField(default=True)
    is_spotlight = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # Import timezone

    def __str__(self):
        """Returns the name of the subscription plan."""
        return self.name


# Extending the User model with profile details
class UserProfile(models.Model):
    """
    Extends the default User model to include additional profile information.

    Attributes:
        user (User): The associated User object.
        name (str): The user's full name.
        username (str): The user's chosen username.
        email (str): The user's email address.
        profile_picture (ImageField): The user's profile picture.
        fitness_goal (str): The user's fitness goal or objective.
        age (int): The user's age.
        phone (str): The user's phone number.
        subscription_status (str): The status of the user's subscription.
        subscription_plan (SubscriptionPlan): The subscription plan the user is enrolled in.
        created_at (datetime): The date and time when the profile was created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100, blank=True)  
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True)  # Add email field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    fitness_goal = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True) 
    phone = models.CharField(max_length=15, blank=True, null=True) 
    subscription_status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')
    subscription_plan = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.SET_NULL)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        """Returns a string representation of the user's profile."""
        return f"{self.user.username}'s Profile"


# Exercise Plan model
class ExercisePlan(models.Model):
    """
    Represents an exercise plan available for users.

    Attributes:
        title (str): The title of the exercise plan.
        description (str): A detailed description of the plan.
        difficulty (str): The difficulty level of the exercise plan.
        duration (Decimal): The duration of the exercise plan in hours or days.
        category (str): The category or type of exercise.
        price (Decimal): The cost of the exercise plan.
        created_at (datetime): The date and time when the plan was created.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title


# Nutrition Plan model
class NutritionPlan(models.Model):
    """
    Represents a nutrition plan available for users.

    Attributes:
        title (str): The title of the nutrition plan.
        description (str): A detailed description of the plan.
        diet_type (str): The type of diet the plan follows.
        price (Decimal): The cost of the nutrition plan.
        calories (str): The total calorie content of the plan.
        created_at (datetime): The date and time when the plan was created.
    """
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
    """
    Represents a product available for purchase, such as merchandise or nutrition products.

    Attributes:
        name (str): The name of the product.
        description (str): A detailed description of the product.
        price (Decimal): The price of the product.
        image (ImageField): An image of the product.
        stock_quantity (int): The quantity of the product in stock.
        is_spotlight (bool): Highlights the product as a featured item.
        created_at (datetime): The date and time when the product was added.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  
    is_spotlight = models.BooleanField(default=False)  # New field for spotlight products

    def __str__(self):
        """Returns the name of the product."""
        return self.name


# Order model for purchases
class Order(models.Model):
    """
    Represents an order placed by a user.

    Attributes:
        user (User): The user who placed the order.
        order_date (datetime): The date and time when the order was placed.
        total_amount (Decimal): The total cost of the order.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
 
    def __str__(self):
        """Returns a string representation of the order."""
        return f"Order {self.id} by {self.user.username}"


# Review model for plans and products
class Review(models.Model):
    """
    Represents a review for a product, submitted by a user.

    Attributes:
        product (Product): The product being reviewed.
        user (User): The user who wrote the review.
        rating (int): The rating given to the product (1 to 5).
        comment (str): The text of the review.
        created_at (datetime): The date and time when the review was created.
        updated_at (datetime): The date and time when the review was last updated.
    """
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of the review."""
        return f'Review for {self.product.name} by {self.user.username}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.product.id)])


# Community Update model
class CommunityUpdate(models.Model):
    """
    Represents a community update posted by a user.

    Attributes:
        user (User): The user who posted the update.
        update_text (str): The text content of the update.
        created_at (datetime): The date and time when the update was posted.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        """Returns a string representation of the community update."""
        return f"Update by {self.user.username}"
from django.db import models

# Define the Wishlist model
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

# Define the WishlistItem model (which references Wishlist)
class WishlistItem(models.Model):
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE, related_name='items')  # 'Wishlist' as a string
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wishlist', 'product')  # Ensure no duplicates

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"
