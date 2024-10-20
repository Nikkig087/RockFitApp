from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Extending the User model with profile details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    fitness_goal = models.CharField(max_length=255, null=True, blank=True)
    subscription_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Subscription Plan model
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    benefits = models.TextField()

    def __str__(self):
        return self.name

# Exercise Plan model
class ExercisePlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

# Nutrition Plan model
class NutritionPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    diet_type = models.CharField(max_length=100)  # e.g. Vegan, Keto
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

# Product model for merchandise and nutrition products
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock_quantity = models.IntegerField()

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

    def __str__(self):
        return f"Review by {self.user.username}"

# Community Update model
class CommunityUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Update by {self.user.username}"

# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
