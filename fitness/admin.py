from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, Wishlist, UserProfile
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html

# Inline for UserProfile to be displayed within User Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'pause_requested', 'pause_approved', 'subscription_plan']
    list_filter = ['pause_requested', 'pause_approved']
    actions = ['approve_pause', 'reject_pause']

    def approve_pause(self, request, queryset):
        """Approve the pause request."""
        queryset.update(pause_approved=True, pause_requested=False)
        self.message_user(request, "Pause request approved.")

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

