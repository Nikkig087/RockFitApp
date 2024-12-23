from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    SubscriptionPlan, UserProfile, Product, Order, Review, Wishlist,
    NewsletterSubscription, ContactMessage, CommunityUpdate
)
from datetime import timedelta, date
from decimal import Decimal
from django.urls import reverse
from unittest.mock import patch
from unittest import mock
from django.utils import timezone
import uuid
import unittest
from cart.models import Cart, CartItem




class ModelsTestCase(TestCase):
    def setUp(self):
        """Common setup for tests."""
        # Use unique username for each test by using self._testMethodName
        self.username = f"testuser_{self._testMethodName}"
        self.user = User.objects.create_user(username=self.username, password="password123")
        self.subscription_plan = SubscriptionPlan.objects.create(
            name="Basic Plan",
            price=Decimal('9.99'),
            duration=30,
            benefits="Access to basic features",
            is_active=True
        )
        self.product = Product.objects.create(
            name="Yoga Mat",
            description="A durable yoga mat.",
            price=Decimal('29.99'),
            stock_quantity=50
        )

    def test_subscription_plan_creation(self):
        """Test the creation of a subscription plan."""
        self.assertEqual(self.subscription_plan.name, "Basic Plan")
        self.assertTrue(self.subscription_plan.is_active)
        self.assertEqual(self.subscription_plan.price, Decimal('9.99'))
        self.assertEqual(self.subscription_plan.duration, 30)

    def test_user_profile_creation(self):
        """Test user profile creation with a subscription."""
        plan = SubscriptionPlan.objects.create(name="Test Plan", price=10, duration=12)

        # Delete any existing profile for the user to avoid UNIQUE constraint errors
        UserProfile.objects.filter(user=self.user).delete()

        # Ensure that the user profile is created with the subscription plan
        profile = UserProfile.objects.create(
            user=self.user,  # Use self.user, which was created in setUp
            name="Test User",
            email="test@example.com",
            subscription_plan=plan,
            subscription_start_date=date.today(),
            subscription_end_date=date.today() + timedelta(days=plan.duration)
        )

        self.assertIsNotNone(profile)  # Make sure the profile was created
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.subscription_plan, plan)

    def test_product_creation(self):
        """Test product creation."""
        self.assertEqual(self.product.name, "Yoga Mat")
        self.assertEqual(self.product.price, Decimal('29.99'))
        self.assertEqual(self.product.stock_quantity, 50)

    def test_order_creation(self):
        """Test order creation."""
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('59.98')
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, Decimal('59.98'))

    def test_review_creation(self):
        """Test review creation."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment="Great quality!"
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great quality!")

    def test_wishlist_and_add_item(self):
        """Test wishlist creation and adding an item."""
        wishlist = Wishlist.objects.create(user=self.user)
        wishlist.products.add(self.product)
        self.assertIn(self.product, wishlist.products.all())

    def test_newsletter_subscription(self):
        """Test newsletter subscription."""
        subscription = NewsletterSubscription.objects.create(email="test@example.com")
        self.assertEqual(subscription.email, "test@example.com")

    def test_contact_message(self):
        """Test contact message submission."""
        message = ContactMessage.objects.create(
            name="Jane Doe",
            email="jane.doe@example.com",
            message="Can I get a trial?"
        )
        self.assertEqual(message.name, "Jane Doe")
        self.assertEqual(message.message, "Can I get a trial?")


class ViewsTestCase(TestCase):
    def setUp(self):
        """Set up for view tests."""
        # Generate a unique username using uuid for each test
        self.username = f'testuser_{uuid.uuid4().hex}'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        self.update = CommunityUpdate.objects.create(content="Test update", user=self.user)
        
        # Create a plan for subscription
        self.plan = SubscriptionPlan.objects.create(name="Test Plan", price=10, duration=12)

        # Create UserProfile for the user if it doesn't exist
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                'name': "Test User",
                'email': "test@example.com",
                'subscription_plan': self.plan,
                'subscription_start_date': date.today(),
                'subscription_end_date': date.today() + timedelta(days=self.plan.duration)
            }
        )

        # Create a product for wishlist tests
        self.product = Product.objects.create(
            name="Test Product",
            description="A product for wishlist testing",
            price=Decimal('19.99'),
            stock_quantity=10
        )

    def test_subscription_view(self):
        """Test the subscription view."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('subscription'))  # Matches 'subscription/' URL
        self.assertEqual(response.status_code, 200)

    def test_subscribe_view(self):
        """Test subscription view with POST request."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('subscribe', args=[self.plan.id]))  # Include plan_id
        self.assertRedirects(response, reverse('profile'))

    def test_add_to_wishlist(self):
        # Generate a unique username for the test
        unique_username = f'testuser_{uuid.uuid4().hex}'
        self.user = User.objects.create_user(username=unique_username, password='password')

        # Authenticate the user
        self.client.login(username=unique_username, password='password')

        # Create a product to add to the wishlist with stock_quantity specified
        product = Product.objects.create(name="Test Product", price=10.99, stock_quantity=10)

        # Send the POST request to add the product to the wishlist
        response = self.client.post(reverse('add_to_wishlist', args=[product.id]))

        # Check that the product is added to the wishlist
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertTrue(wishlist.items.filter(product=product).exists())


    def test_community_updates(self):
        # Delete existing community updates to ensure a clean state
        CommunityUpdate.objects.all().delete()

        # Create a user with a unique username
        unique_username = f'testuser_{uuid.uuid4().hex}'
        user = User.objects.create_user(username=unique_username, password='password')

        # Log in the user
        self.client.login(username=unique_username, password='password')

        # Ensure no community updates exist before creating one
        print(f"Before creating update: {CommunityUpdate.objects.count()}")  # Debugging line

        # Create one community update
        update = CommunityUpdate.objects.create(user=user, content="Test update", created_at=timezone.now())

        # Ensure that the community update was created
        print(f"After creating update: {CommunityUpdate.objects.count()}")  # Debugging line

        # Make a request to the community updates page
        response = self.client.get(reverse('community_updates'))

        # Check if the response contains the correct context and one update
        #print(f"Context updates: {response.context.get('updates', [])}")  # Debugging line

        # Assert that there is exactly one update in the context
        self.assertEqual(len(response.context['updates']), 1)  # We should have exactly 1 update
        self.assertContains(response, "Test update")

    def test_contact_message_creation(self):
        message = ContactMessage.objects.create(
            name="Jane Doe", email="jane.doe@example.com", message="Hello!"
        )
        self.assertEqual(message.name, "Jane Doe")
        self.assertEqual(message.message, "Hello!")
    
   # def test_unauthorized_access_to_subscribe(self):
        # Try accessing the subscription page without being logged in
    #    response = self.client.get(reverse('subscription'))

        # Assert that the response redirects to the login page with the correct next parameter
     #   self.assertRedirects(response, f'/accounts/login/?next={reverse("subscription")}')
class CartTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password123")
        
        # Create a Cart instance
        self.cart = Cart.objects.create(user=self.user)
        
        # Create a Product instance
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product description",
            price=10.99,
            stock_quantity=100
        )
        
        self.subscription = SubscriptionPlan.objects.create(
            name="Monthly Plan", 
            duration=30,  # Assuming the duration is in days or months
            price=19.99  # Provide a non-null value here
        )
        
        # Add a product to the cart
        self.cart_item_product = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        
        # Add a subscription to the cart
        self.cart_item_subscription = CartItem.objects.create(
            cart=self.cart,
            subscription=self.subscription,
            quantity=1
        )

    def test_add_to_cart(self):
        # Verify product item in the cart
        self.assertEqual(self.cart_item_product.product.name, "Test Product")
        self.assertEqual(self.cart_item_product.quantity, 2)

        # Verify subscription item in the cart
        self.assertEqual(self.cart_item_subscription.subscription.name, "Monthly Plan")
        self.assertEqual(self.cart_item_subscription.quantity, 1)

    def test_total_cost(self):
        # Calculate the total cost of the cart
        expected_cost = Decimal(self.product.price * 2) + Decimal(self.subscription.price * 1)
        # Ensure both are Decimal for accurate comparison
        self.assertAlmostEqual(self.cart.get_total_cost(), expected_cost)

    def test_total_items(self):
        # Verify total items in the cart
        expected_items = 2 + 1  # 2 products and 1 subscription
        self.assertEqual(self.cart.get_total_items(), expected_items)

    def test_remove_from_cart(self):
        # Remove product item and check
        self.cart_item_product.delete()
        self.assertFalse(CartItem.objects.filter(id=self.cart_item_product.id).exists())
        
        # Remove subscription item and check
        self.cart_item_subscription.delete()
        self.assertFalse(CartItem.objects.filter(id=self.cart_item_subscription.id).exists())

    def test_view_cart(self):
        # Retrieve cart items and check
        cart_items = self.cart.items.all()
        self.assertEqual(cart_items.count(), 2)

        # Check the product in the cart
        product_item = cart_items.get(product=self.product)
        self.assertEqual(product_item.quantity, 2)
        
        # Check the subscription in the cart
        subscription_item = cart_items.get(subscription=self.subscription)
        self.assertEqual(subscription_item.quantity, 1)
