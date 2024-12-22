from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, UserProfile, Wishlist, WishlistItem
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
from .forms import ReviewForm
from .forms import NewsletterSignupForm,ContactMessageForm
import json
from django.core.mail import send_mail


# Subscription Views
#def subscription_plans(request):
    # Fetch subscription plans from the database
    #subscription_plans = SubscriptionPlan.objects.all()

    # Check if user has a profile (might be empty for some users)
    #try:
     #   user_profile = request.user.userprofile
      #  pause_requested = user_profile.pause_requested
       # pause_approved = user_profile.pause_approved
    #except UserProfile.DoesNotExist:
     #   user_profile = None
      #  pause_requested = False
       # pause_approved = False

    #return render(
     #   request,
      #  'fitness/subscription.html',  # Ensure this is the correct template name
       # {
        ##    'subscription_plans': subscription_plans,
          #  'user_profile': user_profile,
           # 'pause_requested': pause_requested,
            #'pause_approved': pause_approved
       # }
    #)

def subscription_plans(request):
    """
    View to display subscription plans and the user's current subscription state.
    """
    subscription_plans = SubscriptionPlan.objects.all()
    plans = SubscriptionPlan.objects.filter(is_active=True)

    
    user_profile = getattr(request.user, 'userprofile', None)
    current_subscription = user_profile.subscription_plan if user_profile else None
    is_paused = user_profile.pause_approved if user_profile else False

   
    context = {
        'subscription_plans': subscription_plans,
        'user_profile': user_profile,
        'current_subscription': current_subscription,
        'is_paused': is_paused,
        'pause_requested': user_profile.pause_requested if user_profile else False,
        'pause_approved': is_paused, 
    }

    return render(request, 'fitness/subscription.html', context)



@login_required
def subscription_view(request):
    user = request.user
    subscription_plans = SubscriptionPlan.objects.all()
    
    context = {
        'user': user,
        'subscription_plans': subscription_plans,
    }
    return render(request, 'fitness/subscription.html', context)



@login_required
def subscribe(request, plan_id):
    """
    Subscribe the user to a selected subscription plan.
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

@login_required
def cancel_subscription(request):
    """
    Cancel the user's subscription plan.
    """
    subscription_plan = request.user.userprofile.subscription_plan

    if subscription_plan and subscription_plan.is_active:
        request.user.userprofile.subscription_plan = None
        request.user.userprofile.save()
        messages.success(request, "Your subscription has been canceled.")
        return redirect('subscription')
    else:
        return HttpResponseBadRequest("No active subscription to cancel.")

@csrf_protect
@require_POST
def add_subscription_plans(request):
    """
    Add multiple subscription plans from a JSON request.
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



#def request_pause_subscription(request):
 #   ""
  #  Allows a user to request a pause on their subscription.
    
   # user_profile = request.user.userprofile
    #if user_profile.pause_requested or user_profile.pause_approved:
     #   # Prevent requesting a pause if one is already in progress or approved
      #  messages.info(request, "You already have a pause request or it has been approved.")
       # return redirect('profile')

    # If no pause request is pending, set it as requested
   # user_profile.pause_requested = True
   # user_profile.save()
   # messages.info(request, "Your pause request has been submitted for approval.")
   # return redirect('profile')

#from django.utils import timezone
def request_pause_subscription(request):
    user_profile = request.user.userprofile

   
    if not user_profile.pause_requested and request.user.userprofile.subscription_plan.is_active:
        user_profile.pause_requested = True
        user_profile.save()

      
        send_mail(
            'Subscription Pause Request',
            f'{request.user.username} has requested to pause their subscription.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  
        )

        messages.success(request, 'Your subscription pause request has been submitted and is awaiting approval.')
        return redirect('profile')
    else:
        messages.error(request, 'You cannot request to pause your subscription at this time.')
        return redirect('profile')

"""
@login_required
def approve_pause_subscription(request):
    ""
    Approves a user's pause subscription request.
    ""
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to approve pause requests.")
    
    # Assuming admin selects a specific user to approve
    user_id = request.POST.get('user_id')  # Example: ID passed in a form
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    
    if user_profile.pause_requested:
        user_profile.pause_requested = False
        user_profile.pause_approved = True
        user_profile.save()

        messages.success(request, "The subscription pause has been approved.")
    else:
        messages.error(request, "No pause request to approve.")
    
    return redirect('admin_dashboard')  # Replace with actual admin view
"""
@login_required
def resume_subscription(request):
    """Allow users to resume their paused subscription."""
    user_profile = request.user.userprofile
    if user_profile.pause_approved:
       
        user_profile.pause_approved = False  
        user_profile.save()
        messages.success(request, "Your subscription has been resumed.")
    else:
        messages.error(request, "Your subscription was not paused.")
    
    return redirect('profile')

def home(request):
    """
    Display the home page with featured content.
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
    Display a list of products, with search and sorting options.
    """
    query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    valid_sort_fields = ['name', 'price', '-price', 'created_at', '-created_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    products = products.order_by(sort_by)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fitness/product_list.html', {
        'products': products,
        'page_obj': page_obj,
        'query': query,
    })

def product_detail(request, product_id):
    """
    Display detailed information about a specific product.
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product, approved=True)
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
    """
    Adds a product to the user's wishlist.
    """
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    
    return redirect('wishlist_view')

@login_required(login_url='login') 
def wishlist_view(request):
    """
    Displays the user's wishlist.
    """
    wishlist = Wishlist.objects.filter(user=request.user).first()  
    wishlist_items = wishlist.items.all() if wishlist else []  
    return render(request, 'fitness/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, product_id):
    """
    Removes a product from the user's wishlist.
    """
    wishlist = get_object_or_404(Wishlist, user=request.user)
    try:
        wishlist_item = wishlist.items.get(product_id=product_id)
        wishlist_item.delete()
        messages.success(request, "Item removed from your wishlist.")
    except WishlistItem.DoesNotExist:
        messages.error(request, "Item not found in your wishlist.")
    return redirect('wishlist_view')

def wishlist_count(request):
    """
    Returns the count of items in the user's wishlist.
    """
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        count = wishlist.wishlistitem_set.count()
    else:
        count = 0
    return {'wishlist_count': count}


@login_required
def post_update(request):
    """
    Allow authenticated users to post community updates.
    """
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        CommunityUpdate.objects.create(user=request.user, update_text=update_text)
        return redirect('community_updates')
    return render(request, 'fitness/post_update.html')

def community_updates(request):
    """
    Display a list of community updates and handle newsletter subscription/unsubscription.
    """
    updates = CommunityUpdate.objects.order_by('-created_at')

    if request.method == 'POST':
        action = request.POST.get('action')
        email = request.POST.get('email')

        if action == 'subscribe':
            form = NewsletterSignupForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully subscribed to the newsletter!')
            else:
                messages.error(request, 'This email is already subscribed.')

        elif action == 'unsubscribe':
            try:
                subscription = NewsletterSubscription.objects.get(email=email)
                subscription.delete()
                messages.success(request, 'You have successfully unsubscribed from the newsletter.')
            except NewsletterSubscription.DoesNotExist:
                messages.error(request, 'This email is not subscribed.')

        return redirect('community_updates')

    else:
        form = NewsletterSignupForm()

    return render(request, 'fitness/community_updates.html', {
        'updates': updates,
        'form': form
    })

@login_required(login_url='login') 
def profile_view(request):
    user_profile = request.user.userprofile
    subscription = user_profile.subscription_plan if user_profile else None
    pause_requested = user_profile.pause_requested if user_profile else False
    pause_approved = user_profile.pause_approved if user_profile else False

    return render(request, 'fitness/profile.html', {
        'user_profile': user_profile,
        'subscription': subscription,
        'pause_requested': pause_requested,
        'pause_approved': pause_approved,
    })
def update_profile(request):
    """
    Allow users to update their profile information.
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
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            
            messages.success(request, 'Your review has been submitted and is pending approval by an admin.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_create_review.html', {'form': form, 'product': product})

@login_required
def edit_review(request, review_id):
    """
    Allow users to edit their existing review for a product.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.comment = request.POST['comment']
        review.rating = request.POST['rating']
        review.save()
        return redirect('product_detail', product_id=review.product.id)

@login_required
def delete_review(request, review_id):
    """
    Delete a review submitted by the logged-in user.
    """
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect('product_detail', product_id=review.product.id)

    review.delete()
    messages.success(request, 'Your review has been deleted.')
    
    return redirect('product_detail', product_id=review.product.id)


def contact_form(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you for your message. We will get back to you soon!",
            )
            return redirect(
                "home"
            )
        else:
            messages.error(
                request, "There was an error with your submission."
            )
    else:
        form = ContactMessageForm()
    return render(request, "fitness/contact_form.html", {"form": form})

def custom_404_view(request, exception):
    return render(request, "fitness/404.html", status=404)


def privacy_policy(request):
    return render(request, 'fitness/privacy_policy.html')  # Adjust the path if needed