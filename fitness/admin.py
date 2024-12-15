from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, Wishlist, UserProfile, ContactMessage
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from django.dispatch import receiver
from django.db.models.signals import post_save
from .forms import UserProfileForm
from django.db.models.signals import pre_save


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

from django.contrib import admin
from .models import UserProfile
from django.utils.timezone import now


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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm  

    list_display = ['user', 'pause_requested', 'pause_approved', 'subscription_plan']
    list_filter = ['pause_requested', 'pause_approved']
    
    actions = ['approve_pause', 'reject_pause']

    def save_model(self, request, obj, form, change):
        if obj.pause_approved:  
            obj.pause_requested = False
        super().save_model(request, obj, form, change)

    def approve_pause(self, request, queryset):
        for profile in queryset:
            if profile.pause_requested:
                profile.pause_requested = False
                profile.pause_approved = True
                profile.paused_at = timezone.now()  
                profile.save()
                self.message_user(request, f"Pause request for {profile.user.username} has been approved.")
            else:
                self.message_user(request, f"No pause request for {profile.user.username} to approve.")

    approve_pause.short_description = 'Approve selected pause requests'

    def reject_pause(self, request, queryset):
        """Reject the pause request."""
        queryset.update(pause_approved=False, pause_requested=False)
        self.message_user(request, "Pause request rejected.")

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,) 


admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin)  


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
    list_display = ('name', 'price', 'is_active', 'is_spotlight')
    list_filter = ('is_active', 'is_spotlight')
    search_fields = ('name',)

  
    fields = ('name', 'price', 'duration', 'benefits', 'is_active', 'is_spotlight')

   # def save_model(self, request, obj, form, change):
        #"""
        #Override save_model to untick pause_requested when pause_approved is ticked.
        #"""
        # Check if pause_approved has been changed to True
    #    if obj.pause_approved and 'pause_approved' in form.changed_data:
     #       obj.pause_requested = False  # Ensure pause_requested is unticked
        
        # Set paused_at only if it hasn't been set before
      #  if not obj.paused_at:
       #     obj.paused_at = timezone.now()
    
        # Call the parent save_model to persist changes
        #super().save_model(request, obj, form, change)



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


#@receiver(pre_save, sender=SubscriptionPlan)
#def auto_untick_pause_requested(sender, instance, **kwargs):
 #   """
  #  Ensure pause_requested is unticked when pause_approved is True.
   # """
    #if instance.pause_approved:
     #   instance.pause_requested = False  # Automatically untick pause_requested
      #  if not instance.paused_at:
       #     instance.paused_at = timezone.now()  # Set paused_at if not already set