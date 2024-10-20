    # Search functionality
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, Wishlist
#import stripe 
from django.conf import settings
from django.contrib import messages
from django.db.models import Q  # Import Q for complex queries

# Home Page View
def home(request):
    exercise_plans = ExercisePlan.objects.all()
    nutrition_plans = NutritionPlan.objects.all()
    products = Product.objects.all()
    community_updates = CommunityUpdate.objects.order_by('-date')[:5]
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
        'query': query
    })

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

# No delete_product view needed since CRUD is only in admin panel

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

