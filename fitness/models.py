from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from PIL import Image
from cloudinary.models import CloudinaryField
from django.utils.html import format_html

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
        pause_requested (bool): Indicates if a pause request has been made.
        pause_approved (bool): Indicates if the pause request has been
        approved.
        paused_at (datetime): The date and time when the subscription was
        paused (if applicable).
    """

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
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
        subscription_plan (SubscriptionPlan): The subscription plan the user
        is enrolled in.
        created_at (datetime): The date and time when the profile was created.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    username = models.CharField(
        max_length=100, null=True, blank=True
    )
    email = models.EmailField(blank=True)
    profile_picture = ProcessedImageField(
        upload_to="profile_pictures/",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
        blank=True,
        null=True,
    )
    fitness_goal = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(
        max_length=15, blank=True, null=True
    )
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, null=True, on_delete=models.SET_NULL
    )
    subscription_start_date = models.DateField(
        null=True, blank=True
    )
    subscription_end_date = models.DateField(
        null=True, blank=True
    )
    pause_requested = models.BooleanField(default=False)
    pause_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paused_at = models.DateTimeField(null=True, blank=True)
    resume_requested = models.BooleanField(default=False)
    resume_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    profile_picture_webp = ImageSpecField(
        source="profile_picture",
        format="WEBP",
        options={"quality": 90},
    )

    def is_paused(self):
        """Returns if the subscription is paused."""
        return self.pause_approved and self.paused_at is not None

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
    duration = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
    category = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
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
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
    calories = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

'''
class Product(models.Model):
    """
    Represents a product available for purchase.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 85},
    )
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_spotlight = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.ANTIALIAS)

            img.save(self.image.path, quality=85, optimize=True)

            webp_image_path = (
                os.path.splitext(self.image.path)[0] + ".webp"
            )
            img.save(webp_image_path, format="WebP", quality=85)

            self.image.name = os.path.relpath(
                webp_image_path, start="media/"
            )
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"id": self.id})

    def __str__(self):
        return self.name

'''
class Product(models.Model):
    """
    Represents a product available for purchase.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # ✅ Use CloudinaryField instead of ImageField
    image = CloudinaryField("image", blank=True, null=True)

    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_spotlight = models.BooleanField(default=False)

    def image_tag(self):
        """Display image thumbnail in Django Admin"""
        if self.image:
            return format_html(
                f'<img src="{self.image.url}" width="50" height="50" style="object-fit: cover;"/>'
            )
        return "No Image"

    image_tag.short_description = "Image"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"id": self.id})

    def __str__(self):
        return self.name

class Order(models.Model):
    """
    Represents an order placed by a user.

    Attributes:
        user (User): The user who placed the order.
        order_date (datetime): The date and time when the order was placed.
        total_amount (Decimal): The total cost of the order.
    """
  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_orders')
 
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        """Returns a string representation of the order."""
        return f"Order {self.id} by {self.user.username}"


class Review(models.Model):
    """
    Represents a product review written by a user.

    Attributes:
        user (ForeignKey): The user who wrote the review.
        product (ForeignKey): The product being reviewed.
        rating (IntegerField): The rating given to the product, usually on
        a scale (e.g., 1 to 5).
        comment (TextField): The review text or comment provided by the user.
        approved (BooleanField): Indicates whether the review has been approved
        (default is False).
        created_at (DateTimeField): The timestamp when the review was created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
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
    content = models.TextField(default="No content")

    def __str__(self):
        """Returns a string representation of the community update."""
        return f"Update by {self.user.username}"


class Wishlist(models.Model):
    """
    Represents a user's wishlist.

    Attributes:
        user (OneToOneField): The user to whom the wishlist belongs.
        created_at (DateTimeField): The timestamp when the wishlist was
        created.
        products (ManyToManyField): A collection of products that the user has
        added to the wishlist.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class WishlistItem(models.Model):
    """
    Represents an item in a user's wishlist.

    Attributes:
        wishlist (ForeignKey): The wishlist to which the product belongs.
        product (ForeignKey): The product that has been added to the wishlist.
    """

    wishlist = models.ForeignKey(
        "Wishlist",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("wishlist", "product")

    def __str__(self):
        return (
            f"{self.product.name} in "
            f"{self.wishlist.user.username}'s wishlist"
            )


class NewsletterSubscription(models.Model):
    """
    Represents a subscription to the newsletter.
    """

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    """
    Represents a message submitted via a contact form.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.created_at}"
