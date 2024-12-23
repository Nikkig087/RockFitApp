from django.test import TestCase
from django.contrib.auth.models import User
from fitness.models import Product, SubscriptionPlan
from cart.models import Cart, CartItem
from decimal import Decimal

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
