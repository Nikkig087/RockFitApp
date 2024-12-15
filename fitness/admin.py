from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, Wishlist, UserProfile
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from django.dispatch import receiver
from django.db.models.signals import post_save

# Inline for UserProfile to be displayed within User Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

from django.contrib import admin
from .models import UserProfile
from django.utils.timezone import now

# Action to approve pause request
def approve_pause(modeladmin, request, queryset):
    for profile in queryset:
        if profile.pause_requested:
            profile.pause_requested = False
            profile.pause_approved = True
            profile.paused_at = now()  # Record the time when pause was approved
            profile.save()
            modeladmin.message_user(request, f"Pause request for {profile.user.username} has been approved.")
        else:
            modeladmin.message_user(request, f"No pause request for {profile.user.username} to approve.")

approve_pause.short_description = 'Approve selected pause requests'

# Admin class for UserProfile
#class UserProfileAdmin(admin.ModelAdmin):
 #   list_display = ['user', 'subscription_plan', 'pause_requested', 'pause_approved', 'paused_at']
  #  actions = [approve_pause]  # Register the approve_pause action for admin users

#admin.site.register(UserProfile, UserProfileAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'pause_requested', 'pause_approved', 'subscription_plan']
    list_filter = ['pause_requested', 'pause_approved']
    actions = ['approve_pause', 'reject_pause']

def approve_pause_request(request, subscription_id):
    try:
        subscription = Subscription.objects.get(id=subscription_id)

        if subscription.pause_requested and not subscription.pause_approved:
            subscription.pause_approved = True
            subscription.paused_at = timezone.now()
            subscription.save()

            messages.success(request, f'Pause request for {subscription.user.username} has been approved.')
        else:
            messages.error(request, 'No pause request to approve.')

    except Subscription.DoesNotExist:
        messages.error(request, 'Subscription not found.')

    return redirect('admin_dashboard')  # Redirect to admin dashboard or any appropriate page


    def reject_pause(self, request, queryset):
        """Reject the pause request."""
        queryset.update(pause_approved=False, pause_requested=False)
        self.message_user(request, "Pause request rejected.")



class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Add the UserProfile inline

# This registers the customized UserAdmin with additional UserProfile inline
admin.site.unregister(User)  # Unregister the default User model
admin.site.register(User, CustomUserAdmin)  # Register with the customized admin


@admin.register(ExercisePlan)
class ExercisePlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'created_at')
    search_fields = ('title',)

@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'calories', 'created_at')
    search_fields = ('title',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_spotlight',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')


@admin.register(CommunityUpdate)
class CommunityUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'update_text', 'created_at')
    search_fields = ('update_text',)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'is_spotlight', 'pause_requested', 'pause_approved', 'paused_at', 'resume_requested', 'resume_approved')
    list_filter = ('is_active', 'is_spotlight', 'pause_requested', 'pause_approved')
    search_fields = ('name',)

    # Allow pause-related fields to be edited in the admin panel
    fields = ('name', 'price', 'duration', 'benefits', 'is_active', 'is_spotlight', 'pause_requested', 'pause_approved', 'paused_at', 'resume_requested', 'resume_approved')

    def save_model(self, request, obj, form, change):
        # When saving, check if pause_requested is set and update paused_at field accordingly
        if obj.pause_requested and not obj.paused_at:
            obj.paused_at = timezone.now()  # Set the current time as paused_at
        super().save_model(request, obj, form, change)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ContactMessage instances.

    This customization allows for viewing contact messages submitted by users.

    Attributes:
        readonly_fields: Fields that cannot be edited in the admin interface.
        list_display: Fields to display in the list view.
        search_fields: Fields to include in the search functionality.
        list_filter: Fields to filter by in the list view.
    """

    readonly_fields = ("name", "email", "message", "created_at")
    list_display = ("name", "email", "message", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("name", "created_at")
