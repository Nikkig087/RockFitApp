from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Review, SubscriptionPlan, Cart, Order

class RockFitAppTests(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.user = User.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(name="Test Product", price=50.0)
        self.subscription_plan = SubscriptionPlan.objects.create(name="Premium Plan", price=9.99)
        self.cart = Cart.objects.create(user=self.user)
    
    # Test for "Subscribe to a Plan"
    def test_subscribe_to_plan(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('subscribe'), {'plan_id': self.subscription_plan.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Checkout")

    # Test for "View Subscription Plans"
    def test_view_subscription_plans(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('subscriptions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.subscription_plan.name)

    # Test for "Forgot Password"
    def test_forgot_password(self):
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password reset instructions sent")

    # Test for "View and Edit Account Details"
    def test_view_edit_account_details(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        
        response = self.client.post(reverse('profile'), {'username': 'newusername'})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    # Test for "Login"
    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('home')))

    # Test for "Dynamic Cart Icon Update"
    def test_cart_icon_update(self):
        self.client.login(username="testuser", password="password")
        self.cart.products.add(self.product)
        response = self.client.get(reverse('cart'))
        self.assertContains(response, "1 item")

    # Test for "Remove Item from Cart"
    def test_remove_item_from_cart(self):
        self.cart.products.add(self.product)
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('remove_from_cart'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.cart.products.count(), 0)

    # Test for "Update Quantity in Cart"
    def test_update_quantity_in_cart(self):
        self.cart.products.add(self.product)
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('update_cart'), {'product_id': self.product.id, 'quantity': 2})
        self.assertEqual(response.status_code, 302)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.first().quantity, 2)

    # Test for "View Total Price of Items in Cart"
    def test_total_price_in_cart(self):
        self.cart.products.add(self.product)
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('cart'))
        self.assertContains(response, "Total: $50.00")

    # Test for "Add Product to Cart"
    def test_add_product_to_cart(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('add_to_cart'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.cart.products.count(), 1)

    # Test for "Create, Edit, Delete Reviews"
    def test_manage_reviews(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('add_review', args=[self.product.id]), {'rating': 5, 'comment': 'Great product!'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.reviews.count(), 1)

        review = self.product.reviews.first()
        response = self.client.post(reverse('edit_review', args=[review.id]), {'rating': 4, 'comment': 'Good product!'})
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.rating, 4)

        response = self.client.post(reverse('delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.reviews.count(), 0)

    # Test for "View Customer Reviews and Ratings"
    def test_view_reviews(self):
        Review.objects.create(product=self.product, user=self.user, rating=5, comment="Excellent!")
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertContains(response, "Excellent!")

    # Test for "See Product Images"
    def test_product_images(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, self.product.image.url)

    # Test for "Sort Products"
    def test_sort_products(self):
        response = self.client.get(reverse('product_list') + '?sort=price')
        self.assertEqual(response.status_code, 200)

    # Test for "Search Products"
    def test_search_products(self):
        response = self.client.get(reverse('product_list') + '?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    # Test for "View List of Products"
    def test_view_products(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, self.product.name)
