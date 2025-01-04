"""
Unit tests for models and views in the application.

This module tests the functionality of various models and views, including
SubscriptionPlan, UserProfile, Product, Order, Review, Wishlist,
NewsletterSubscription,
ContactMessage, CommunityUpdate, and the Cart system.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    SubscriptionPlan,
    UserProfile,
    Product,
    Order,
    Review,
    Wishlist,
    NewsletterSubscription,
    ContactMessage,
    CommunityUpdate,
    WishlistItem,
)
from datetime import timedelta, date
from decimal import Decimal
from django.urls import reverse
from unittest.mock import patch
from unittest import mock
from django.utils import timezone
import uuid
from cart.models import Cart, CartItem


class ModelsTestCase(TestCase):
    """
    Unit tests for various models in the application.
    """

    def setUp(self):
        """Set up test data for models."""
        self.username = f"testuser_{self._testMethodName}"
        self.user = User.objects.create_user(
            username=self.username, password="password123"
        )
        self.subscription_plan = SubscriptionPlan.objects.create(
            name="Basic Plan",
            price=Decimal("9.99"),
            duration=30,
            benefits="Access to basic features",
            is_active=True,
        )
        self.product = Product.objects.create(
            name="Yoga Mat",
            description="A durable yoga mat.",
            price=Decimal("29.99"),
            stock_quantity=50,
        )

    def test_subscription_plan_creation(self):
        """Test the creation of a SubscriptionPlan instance."""
        self.assertEqual(
            self.subscription_plan.name, "Basic Plan"
        )
        self.assertTrue(self.subscription_plan.is_active)
        self.assertEqual(
            self.subscription_plan.price, Decimal("9.99")
        )
        self.assertEqual(self.subscription_plan.duration, 30)

    def test_user_profile_creation(self):
        """Test the creation of a UserProfile with a subscription plan."""
        plan = SubscriptionPlan.objects.create(
            name="Test Plan", price=10, duration=12
        )
        UserProfile.objects.filter(user=self.user).delete()
        profile = UserProfile.objects.create(
            user=self.user,
            name="Test User",
            email="test@example.com",
            subscription_plan=plan,
            subscription_start_date=date.today(),
            subscription_end_date=date.today()
            + timedelta(days=plan.duration),
        )
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.subscription_plan, plan)

    def test_product_creation(self):
        """Test the creation of a Product instance."""
        self.assertEqual(self.product.name, "Yoga Mat")
        self.assertEqual(self.product.price, Decimal("29.99"))
        self.assertEqual(self.product.stock_quantity, 50)

    def test_order_creation(self):
        """Test the creation of an Order instance."""
        order = Order.objects.create(
            user=self.user, total_amount=Decimal("59.98")
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, Decimal("59.98"))

    def test_review_creation(self):
        """Test the creation of a Review instance."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment="Great quality!",
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great quality!")

    def test_wishlist_and_add_item(self):
        """Test the creation of a Wishlist and adding a Product to it."""
        wishlist = Wishlist.objects.create(user=self.user)
        wishlist.products.add(self.product)
        self.assertIn(self.product, wishlist.products.all())

    def test_newsletter_subscription(self):
        """Test the creation of a NewsletterSubscription."""
        subscription = NewsletterSubscription.objects.create(
            email="test@example.com"
        )
        self.assertEqual(subscription.email, "test@example.com")

    def test_contact_message(self):
        """Test the creation of a ContactMessage."""
        message = ContactMessage.objects.create(
            name="Jane Doe",
            email="jane.doe@example.com",
            message="Can I get a trial?",
        )
        self.assertEqual(message.name, "Jane Doe")
        self.assertEqual(message.message, "Can I get a trial?")


class ViewsTestCase(TestCase):
    """
    Unit tests for various views in the application.
    """

    def setUp(self):
        """Set up test data for views."""
        self.username = f"testuser_{uuid.uuid4().hex}"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.update = CommunityUpdate.objects.create(
            content="Test update", user=self.user
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Test Plan", price=10, duration=12
        )
        self.user_profile, created = (
            UserProfile.objects.get_or_create(
                user=self.user,
                defaults={
                    "name": "Test User",
                    "email": "test@example.com",
                    "subscription_plan": self.plan,
                    "subscription_start_date": date.today(),
                    "subscription_end_date": date.today()
                    + timedelta(days=self.plan.duration),
                },
            )
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="A product for wishlist testing",
            price=Decimal("19.99"),
            stock_quantity=10,
        )

    def test_subscription_view(self):
        """Test the subscription view for authenticated users."""
        self.client.login(
            username=self.username, password=self.password
        )
        response = self.client.get(reverse("subscription"))
        self.assertEqual(response.status_code, 200)

    def test_subscribe_view(self):
        """Test subscribing to a plan via POST request."""
        self.client.login(
            username=self.username, password=self.password
        )
        response = self.client.post(
            reverse("subscribe", args=[self.plan.id])
        )
        self.assertRedirects(response, reverse("profile"))

    def test_add_to_wishlist(self):
        """Test adding a Product to the Wishlist."""
        unique_username = f"testuser_{uuid.uuid4().hex}"
        self.user = User.objects.create_user(
            username=unique_username, password="password"
        )

        self.client.login(
            username=unique_username, password="password"
        )

        product = Product.objects.create(
            name="Test Product", price=10.99, stock_quantity=10
        )

        wishlist, created = Wishlist.objects.get_or_create(
            user=self.user
        )

        response = self.client.post(
            reverse("add_to_wishlist", args=[product.id])
        )

        wishlist.refresh_from_db()

        wishlist_item_exists = WishlistItem.objects.filter(
            wishlist=wishlist, product=product
        ).exists()

        self.assertTrue(wishlist_item_exists)

    def test_community_updates(self):
        """Test retrieving community updates."""
        CommunityUpdate.objects.all().delete()
        unique_username = f"testuser_{uuid.uuid4().hex}"
        user = User.objects.create_user(
            username=unique_username, password="password"
        )
        self.client.login(
            username=unique_username, password="password"
        )
        update = CommunityUpdate.objects.create(
            user=user,
            content="Test update",
            created_at=timezone.now(),
        )
        response = self.client.get(reverse("community_updates"))
        self.assertEqual(len(response.context["updates"]), 1)
        self.assertContains(response, "Test update")


class CartTests(TestCase):
    """
    Unit tests for Cart and CartItem functionality.
    """

    def setUp(self):
        """Set up test data for Cart functionality."""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product description",
            price=10.99,
            stock_quantity=100,
        )
        self.subscription = SubscriptionPlan.objects.create(
            name="Monthly Plan", duration=30, price=19.99
        )
        self.cart_item_product = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )
        self.cart_item_subscription = CartItem.objects.create(
            cart=self.cart,
            subscription=self.subscription,
            quantity=1,
        )

    def test_add_to_cart(self):
        """Test adding items to the Cart."""
        self.assertEqual(
            self.cart_item_product.product.name, "Test Product"
        )
        self.assertEqual(self.cart_item_product.quantity, 2)
        self.assertEqual(
            self.cart_item_subscription.subscription.name,
            "Monthly Plan",
        )
        self.assertEqual(self.cart_item_subscription.quantity, 1)

    def test_total_cost(self):
        """Test calculating the total cost of the Cart."""
        expected_cost = Decimal(
            self.product.price * 2
        ) + Decimal(self.subscription.price * 1)
        self.assertAlmostEqual(
            self.cart.get_total_cost(), expected_cost
        )

    def test_total_items(self):
        """Test calculating the total number of items in the Cart."""
        expected_items = 2 + 1
        self.assertEqual(
            self.cart.get_total_items(), expected_items
        )

    def test_remove_from_cart(self):
        """Test removing items from the Cart."""
        self.cart_item_product.delete()
        self.assertFalse(
            CartItem.objects.filter(
                id=self.cart_item_product.id
            ).exists()
        )
        self.cart_item_subscription.delete()
        self.assertFalse(
            CartItem.objects.filter(
                id=self.cart_item_subscription.id
            ).exists()
        )

    def test_view_cart(self):
        """Test retrieving items in the Cart."""
        cart_items = self.cart.items.all()
        self.assertEqual(cart_items.count(), 2)
        product_item = cart_items.get(product=self.product)
        self.assertEqual(product_item.quantity, 2)
        subscription_item = cart_items.get(
            subscription=self.subscription
        )
        self.assertEqual(subscription_item.quantity, 1)
