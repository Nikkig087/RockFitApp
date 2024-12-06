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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Returns the name of the subscription plan."""
        return self.name


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
    is_spotlight = models.BooleanField(default=False)  

    def __str__(self):
        """Returns the name of the product."""
        return self.name



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


class Review(models.Model):
    """
    Represents a product review written by a user.

    This model stores information about a review made by a user for a particular product. 
    It includes the user's rating, a comment, and whether the review is approved. The 
    review also records the timestamp of when it was created.

    Attributes:
        user (ForeignKey): The user who wrote the review.
        product (ForeignKey): The product being reviewed.
        rating (IntegerField): The rating given to the product, usually on a scale (e.g., 1 to 5).
        comment (TextField): The review text or comment provided by the user.
        approved (BooleanField): Indicates whether the review has been approved (default is False).
        created_at (DateTimeField): The timestamp when the review was created.

    Methods:
        __str__: Returns a string representation of the review, indicating the user and the product being reviewed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    approved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the review.

        This method returns a human-readable string that includes the username of the reviewer
        and the name of the product being reviewed.

        Returns:
            str: A string indicating the reviewer's username and the product name.
        """
        return f"Review by {self.user.username} for {self.product.name}"




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

class Wishlist(models.Model):
    """
    Represents a user's wishlist.

    This model stores a wishlist for a user, which contains a collection of products the user 
    wants to keep track of. It uses a one-to-one relationship with the `User` model to ensure 
    that each user can only have one wishlist. The wishlist also records the creation date.

    Attributes:
        user (OneToOneField): The user to whom the wishlist belongs.
        created_at (DateTimeField): The timestamp when the wishlist was created.
        products (ManyToManyField): A collection of products that the user has added to the wishlist.

    Methods:
        __str__: Returns a string representation of the wishlist, indicating the username of the owner.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        """
        Returns a string representation of the wishlist.

        This method returns a human-readable string indicating the username of the user who 
        owns the wishlist.

        Returns:
            str: A string representing the user's wishlist.
        """
        return f"{self.user.username}'s Wishlist"


class WishlistItem(models.Model):
    """
    Represents an item in a user's wishlist.

    This model stores the relationship between a specific product and a user's wishlist. It 
    connects a `Product` to a `Wishlist` and ensures that each product appears only once 
    in the wishlist using the unique constraint.

    Attributes:
        wishlist (ForeignKey): The wishlist to which the product belongs.
        product (ForeignKey): The product that has been added to the wishlist.

    Meta:
        unique_together: Ensures that a product can only appear once in a wishlist by enforcing 
                          a unique constraint on the combination of `wishlist` and `product`.

    Methods:
        __str__: Returns a string representation of the wishlist item, indicating the product name 
                 and the owner of the wishlist.
    """
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wishlist', 'product')  # Ensure no duplicates

    def __str__(self):
        """
        Returns a string representation of the wishlist item.

        This method returns a human-readable string indicating the product name and the 
        username of the user who owns the wishlist.

        Returns:
            str: A string representing the wishlist item and the user's wishlist.
        """
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email