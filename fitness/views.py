"""
Views for the fitness application.

This module defines the views that handle user interactions with the fitness application,
including subscription management, product viewing, wishlist handling, community updates,
and user profiles. Each view function manages a specific part of the application’s functionality.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, UserProfile, Wishlist, WishlistItem, Product 
from django.views.decorators.csrf import csrf_exempt
from .forms import UserProfileForm
from django.conf import settings
from django.contrib import messages
from django.db.models import Q  
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Avg
from django.views import View
from django.views.decorators.csrf import csrf_protect 
from django.views.decorators.http import require_POST  
from django.utils import timezone

import json

from django.shortcuts import render, get_object_or_404
from .models import SubscriptionPlan

def subscription_plans(request):
    """
    Display all active subscription plans.

    Retrieves active subscription plans from the database and renders them on the subscription page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'subscription.html' template with active plans.
    """
    plans = SubscriptionPlan.objects.filter(is_active=True)

    return render(request, 'fitness/subscription.html', {'plans': plans})

@login_required
def subscribe(request, plan_id):
    """
    Subscribe the user to a selected subscription plan.

    Checks if the user is already subscribed and handles the subscription accordingly.

    Args:
        request (HttpRequest): The HTTP request object.
        plan_id (int): The ID of the subscription plan to subscribe to.

    Returns:
        HttpResponse: Redirects to the profile page with a success or error message.
    """
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    user_profile = request.user.userprofile

    if user_profile.subscription_plan:
        current_plan = user_profile.subscription_plan
        if current_plan.is_active:
            messages.error(request, f"You are already subscribed to the {current_plan.name} plan. Please cancel it before switching.")
            return redirect('profile')
        else:
            user_profile.subscription_plan = plan
            user_profile.save()
            messages.success(request, f"Successfully switched to {plan.name} plan!")
    else:
        user_profile.subscription_plan = plan
        user_profile.save()
        messages.success(request, f"You've successfully subscribed to the {plan.name} plan!")
    return redirect('profile')


def cancel_subscription(request):
    """
    Cancel the user's active subscription plan.

    Sets the subscription status to inactive and records the cancellation date.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the subscription page with a success or error message.
    """
    user_profile = request.user.userprofile
    subscription = user_profile.subscription_plan

    if subscription and subscription.is_active:
        subscription.is_active = False
        subscription.end_date = timezone.now().date()  
        subscription.save()
        messages.success(request, "Your subscription has been canceled successfully.")
    else:
        messages.error(request, "You don't have an active subscription to cancel.")
    
    return redirect('subscription')

@csrf_protect  
@require_POST 
def add_subscription_plans(request):
    """
    Add multiple subscription plans from a JSON request.

    Expects a JSON object with a list of plans, each containing name, price, duration, and benefits.

    Args:
        request (HttpRequest): The HTTP request object with JSON data.

    Returns:
        JsonResponse: Returns a success or error message based on the outcome.
    """
    try:
        data = json.loads(request.body)
        if 'plans' not in data:
            return JsonResponse({"status": "error", "message": "No plans data provided"}, status=400)
        
        for plan in data['plans']:
            
            if not all(key in plan for key in ('name', 'price', 'duration', 'benefits')):
                return JsonResponse({"status": "error", "message": "Missing required plan fields"}, status=400)
            
            
            SubscriptionPlan.objects.create(
                name=plan['name'],
                price=plan['price'],
                duration=plan['duration'],
                benefits=plan['benefits']
            )
        
        
        return JsonResponse({"status": "success", "message": "Plans added successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
    
    except Exception as e:

        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def home(request):
    """
    Display the home page with featured content.

    Retrieves exercise plans, nutrition plans, spotlight products, and community updates to display on the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home.html' template with the retrieved data.
    """
    exercise_plans = ExercisePlan.objects.all()
    nutrition_plans = NutritionPlan.objects.all()
    products = Product.objects.all()[:6]  
    spotlight_products = Product.objects.filter(is_spotlight=True)[:6]  
    community_updates = CommunityUpdate.objects.order_by('-created_at')[:5]
    spotlight_subscriptions = SubscriptionPlan.objects.filter(is_spotlight=True)[:3]

    return render(request, 'fitness/home.html', {
        'exercise_plans': exercise_plans,
        'nutrition_plans': nutrition_plans,
        'products': products,
        'spotlight_products': spotlight_products,
        'community_updates': community_updates,
        'spotlight_subscriptions': spotlight_subscriptions,
    })

def products(request):
    """
    Display a list of products with search and sorting functionality.

    Supports pagination and allows users to search for products by name or description.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'product_list.html' template with the filtered and paginated products.
    """
    query = request.GET.get('search', '')  
    sort_by = request.GET.get('sort', 'name')  
    products = Product.objects.all()
    paginator = Paginator(products, 6)  

    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    products = products.order_by(sort_by)  

    product_count = products.count()

    return render(request, 'fitness/product_list.html', {
        'products': products, 
        'product_count': product_count, 
        'query': query,
        'page_obj': page_obj,
    })



def product_detail(request, product_id):
    """
    Display detailed information about a specific product.

    Retrieves product details, associated reviews, and calculates the average rating.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to display.

    Returns:
        HttpResponse: Renders the 'product_detail.html' template with product details and reviews.
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if request.method == 'POST':
        if 'add_to_cart' in request.POST: 
            return redirect('cart:cart_detail')
        
        elif 'add_to_wishlist' in request.POST:
            
            if request.user.is_authenticated:
                Wishlist.objects.get_or_create(user=request.user, product=product)
                return redirect('wishlist') 

    return render(request, 'fitness/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
    }) 
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    # Add the product to the wishlist
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    
    return redirect('view_wishlist')

def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user)  # Correct filtering
    return render(request, 'fitness/wishlist.html', {'wishlist_items': wishlist_items})


def remove_from_wishlist(request, product_id):
    # Get the wishlist for the current user
    wishlist = get_object_or_404(Wishlist, user=request.user)  
    
    try:
        
        wishlist_item = wishlist.items.get(product_id=product_id)  # Now using 'items'
        wishlist_item.delete()  # Delete the item from the wishlist
    except WishlistItem.DoesNotExist:
        print(f"No WishlistItem found for product_id: {product_id} and user: {request.user.id}")
        return redirect('view_wishlist')  # Redirect back to the wishlist page if not found
    
    return redirect('view_wishlist')  # Redirect back to the wishlist page

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        count = wishlist.wishlistitem_set.count()  # Get count of wishlist items
    else:
        count = 0
    return {'wishlist_count': count}

@login_required
def post_update(request):
    """
    Allow authenticated users to post community updates.

    Handles POST requests to create a new community update. If the request is 
    successful, the user is redirected to the community updates page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to 'community_updates' on success or 
                      renders the 'post_update.html' template for GET requests.
    """
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        CommunityUpdate.objects.create(user=request.user, update_text=update_text)
        return redirect('community_updates')
    return render(request, 'fitness/post_update.html')


def community_updates(request):
    """
    Display a list of community updates.

    Retrieves all community updates from the database, ordered by the 
    creation date in descending order.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'community_updates.html' template with the updates.
    """
    updates = CommunityUpdate.objects.order_by('-created_at')
    return render(request, 'fitness/community_updates.html', {'updates': updates})


def profile_view(request):
    """
    Display the user's profile information.

    Retrieves the user's profile data and renders it on the profile page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'profile.html' template with the user's profile data.
    """
    user_profile = request.user.userprofile  
    return render(request, 'fitness/profile.html', {'user_profile': user_profile})

def update_profile(request):
    """
    Allow users to update their profile information.

    Handles POST requests to update the user's profile with data from the submitted form.
    For GET requests, it pre-fills the form with the user's current profile information.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to 'profile' on successful update or 
                      renders the 'update_profile.html' template with the form.
    """
    user_profile = request.user.userprofile  
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'fitness/update_profile.html', {'form': form})


@login_required
def create_review(request, product_id):
    """
    Allow users to create a review for a product.

    Handles POST requests to create a new review for a specified product. 
    Ensures the review is associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product being reviewed.

    Returns:
        HttpResponse: Redirects to the product detail page after successful creation.
                      Renders the 'product_create_review.html' template with the form on GET requests.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_create_review.html', {'form': form, 'product': product})


@login_required
def edit_review(request, review_id):
    """
    Allow users to edit their existing review for a product.

    Ensures that only the user who created the review can edit it. Handles POST requests
    to update the review data.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): The ID of the review to be edited.

    Returns:
        HttpResponse: Redirects to the product detail page after successful update.
                      Renders the 'product_edit_review.html' template with the form on GET requests.
    """
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        return redirect('product_detail', product_id=review.product.id)  
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'product_edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    """
    Allow users to delete their existing review for a product.

    Ensures that only the user who created the review can delete it. Handles POST requests
    to delete the review.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): The ID of the review to be deleted.

    Returns:
        HttpResponse: Redirects to the product detail page after successful deletion.
                      Renders the 'product_delete_review.html' template for GET requests.
    """
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        return redirect('product_detail', product_id=review.product.id)  
    
    if request.method == 'POST':
        review.delete()
        return redirect('product_detail', product_id=review.product.id)
    
    return render(request, 'product_delete_review.html', {'review': review})

    
def add_review(request, product_id):
    """
    Add a review for a specified product.

    Handles POST requests to create a review with user-provided rating and comment.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product being reviewed.

    Returns:
        HttpResponse: Redirects to the product detail page after successful review creation.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')


        review = Review.objects.create(
            user=request.user,
            product=product,
            comment=comment,
            rating=rating
        )
        messages.success(request, 'Your review has been added successfully!')
        return redirect('product_detail', product_id=product.id)

    return redirect('product_detail', product_id=product.id)