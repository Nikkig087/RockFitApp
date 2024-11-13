from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, UserProfile, Wishlist, WishlistItem, Product 
from django.views.decorators.csrf import csrf_exempt
from .forms import UserProfileForm
#import stripe 
from django.conf import settings
from django.contrib import messages
from django.db.models import Q  
from django.http import JsonResponse

from django.db.models import Avg
from django.views import View
from django.views.decorators.csrf import csrf_protect  # Use CSRF protection in production
from django.views.decorators.http import require_POST  # Ensure only POST requests are allowed

import json



# views.py
from django.shortcuts import render, get_object_or_404
from .models import SubscriptionPlan

def subscription_plans(request):
    # Fetch all subscription plans from the database
    plans = SubscriptionPlan.objects.all()

    # Render the subscription plans to the subscription.html template
    return render(request, 'fitness/subscription.html', {'plans': plans})

def subscribe(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    # Assuming you have a user and a UserProfile that holds subscription
    if request.user.is_authenticated:
        # Add the subscription to the user profile
        user_profile = request.user.userprofile
        user_profile.subscription_plan = plan
        user_profile.save()

        # Provide a success message
        messages.success(request, f"You've successfully subscribed to the {plan.name} plan!")
        
        # Redirect the user to their profile page, for example
        return redirect('profile')  # Replace with your actual profile view name
    else:
        # If the user is not authenticated, show an error
        messages.error(request, "You need to be logged in to subscribe.")
        return redirect('login')  # Redirect to login page if not logged in


@csrf_protect  # This ensures CSRF protection is enforced
@require_POST  # This decorator ensures only POST requests are accepted
def add_subscription_plans(request):
    try:
        # Load JSON data from the request
        data = json.loads(request.body)
        
        # Check if 'plans' key exists in the data
        if 'plans' not in data:
            return JsonResponse({"status": "error", "message": "No plans data provided"}, status=400)
        
        # Iterate through the list of plans and create each subscription plan
        for plan in data['plans']:
            # Validate that all required fields are in the plan data
            if not all(key in plan for key in ('name', 'price', 'duration', 'benefits')):
                return JsonResponse({"status": "error", "message": "Missing required plan fields"}, status=400)
            
            # Create SubscriptionPlan objects
            SubscriptionPlan.objects.create(
                name=plan['name'],
                price=plan['price'],
                duration=plan['duration'],
                benefits=plan['benefits']
            )
        
        # If successful, return a success message
        return JsonResponse({"status": "success", "message": "Plans added successfully"})

    except json.JSONDecodeError:
        # Handle JSON decoding errors
        return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
    
    except Exception as e:
        # Handle other exceptions
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# Home Page View
def home(request):
    exercise_plans = ExercisePlan.objects.all()
    nutrition_plans = NutritionPlan.objects.all()
    products = Product.objects.all()
    community_updates = CommunityUpdate.objects.order_by('-created_at')[:5]
    return render(request, 'fitness/home.html', {
        'exercise_plans': exercise_plans,
        'nutrition_plans': nutrition_plans,
        'products': products,
        'community_updates': community_updates,
    })

# View to display all products (read-only for regular users)
def products(request):
    query = request.GET.get('search', '')  # Get search query from URL
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    products = Product.objects.all()

    # Search functionality
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Sorting functionality
    products = products.order_by(sort_by)  # Order products based on sort parameter

    # Count of products
    product_count = products.count()

    return render(request, 'fitness/product_list.html', {
        'products': products, 
        'product_count': product_count, 
        'query': query,
    })



#def view_cart(request):
 #   if request.user.is_authenticated:
  #      cart, created = Cart.objects.get_or_create(user=request.user)
   #     cart_items = cart.items.all()
    #    total_cost = cart.get_total_cost()
     #   return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})
  #  else:
   #     # Redirect to login page if the user is not authenticated
    #    return redirect('login') 



#@login_required
#def remove_from_cart(request, cart_item_id):
 #   cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
  #  cart_item.delete()
   # return redirect('cart:view_cart')

#@login_required
#def update_cart_item(request, cart_item_id):
 #   cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
  #  if request.method == 'POST':
   #     new_quantity = int(request.POST.get('quantity'))
    #    cart_item.quantity = new_quantity
     #   cart_item.save()
    
   # return redirect('cart:view_cart')

# View for displaying a single product and its reviews

def product_detail(request, product_id):
    # Fetch the product based on its ID
    product = get_object_or_404(Product, id=product_id)
    
    # Get all reviews related to this product
    reviews = Review.objects.filter(product=product)
    
    # Calculate average rating if there are reviews
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # If a user is logged in, allow adding to cart or wishlist
    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            # Logic to add product to cart
            
            # cart.add(product, quantity=1) 
            return redirect('cart:cart_detail')  # Redirect to cart page or refresh the page
        
        elif 'add_to_wishlist' in request.POST:
            # Logic to add product to the wishlist
            if request.user.is_authenticated:
                Wishlist.objects.get_or_create(user=request.user, product=product)
                return redirect('wishlist')  # Redirect to the wishlist page

    return render(request, 'fitness/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
    })


# View for subscriptions
#@login_required
#def subscription(request):
   # plans = SubscriptionPlan.objects.all()
    #return render(request, 'fitness/subscription.html', {'plans': plans})

# Add product to wishlist
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

# Post community update
@login_required
def post_update(request):
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        CommunityUpdate.objects.create(user=request.user, update_text=update_text)
        return redirect('community_updates')
    return render(request, 'fitness/post_update.html')

# View community updates
def community_updates(request):
    updates = CommunityUpdate.objects.order_by('-created_at')
    return render(request, 'fitness/community_updates.html', {'updates': updates})

# Update Profile View
'''
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'fitness/update_profile.html', {'form': form})

    products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Sorting functionality
    products = products.order_by(sort_by)  # Order products based on sort parameter

    # Count of products
    product_count = products.count()

    return render(request, 'fitness/products.html', {'products': products, 'product_count': product_count, 'query': query})


# View for subscriptions
@login_required
def subscription(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'fitness/subscription.html', {'plans': plans})


# Add product to wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

# View wishlist
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'fitness/wishlist.html', {'wishlist_items': wishlist_items})

# Post community update
@login_required
def post_update(request):
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        CommunityUpdate.objects.create(user=request.user, update_text=update_text)
        return redirect('community_updates')
    return render(request, 'fitness/post_update.html')

# View community updates
def community_updates(request):
    updates = CommunityUpdate.objects.order_by('-date')
    return render(request, 'fitness/community_updates.html', {'updates': updates})

# Update Profile View
@login_required
def update_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'fitness/update_profile.html', {'form': form})
'''

#def add_to_cart(request, product_id):
 #   product = get_object_or_404(Product, id=product_id)

  #  if request.user.is_authenticated:
        # Get or create a cart for the user
   #     cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product already exists in the cart
    #    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

     #   if not created:
            # If item already exists, increment the quantity
      #      cart_item.quantity += 1
       #     cart_item.save()
        #else:
            # New item, set quantity to 1
         #   cart_item.quantity = 1
          #  cart_item.save()

      #  messages.success(request, f"{product.name} has been added to your cart!")

  #  else:
        # For unauthenticated users, continue using session
   #     cart = request.session.get('cart', {})
    #    if str(product_id) in cart:
     #       cart[str(product_id)] += 1
     #   else:
      #      cart[str(product_id)] = 1

      #  request.session['cart'] = cart
     #   request.session.modified = True
      #  messages.success(request, "Item added to your cart!")

 #   return redirect('product_list')  # Ensure this is the correct URL name
#@login_required
#def profile(request):
   
 #   return render(request, 'fitness/profile.html')

def profile_view(request):
    user_profile = request.user.userprofile  # Get the logged-in user's profile
    return render(request, 'fitness/profile.html', {'user_profile': user_profile})

def update_profile(request):
    user_profile = request.user.userprofile  # Get the logged-in user's profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after updating
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'fitness/update_profile.html', {'form': form})

# Create Review
@login_required
def create_review(request, product_id):
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

# Edit Review
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        return redirect('product_detail', product_id=review.product.id)  # Prevent others from editing
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'product_edit_review.html', {'form': form, 'review': review})

# Delete Review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        return redirect('product_detail', product_id=review.product.id)  # Prevent others from deleting
    
    if request.method == 'POST':
        review.delete()
        return redirect('product_detail', product_id=review.product.id)
    
    return render(request, 'product_delete_review.html', {'review': review})

    # Add Review view
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # Create the review
        review = Review.objects.create(
            user=request.user,
            product=product,
            comment=comment,
            rating=rating
        )
        messages.success(request, 'Your review has been added successfully!')
        return redirect('product_detail', product_id=product.id)

    return redirect('product_detail', product_id=product.id)