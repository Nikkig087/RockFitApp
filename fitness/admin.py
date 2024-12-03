# Register your models here.
from django.contrib import admin
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, Wishlist, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



# Inline admin for UserProfile
'''
This module customizes the Django admin site for the models specified below
'''
class UserProfileInline(admin.StackedInline):  # Or admin.TabularInline
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('name', 'email', 'profile_picture', 'fitness_goal', 'age', 'phone', 'subscription_status','subscription_plan')  # Add subscription_plan
    max_num = 1  # Only allow one UserProfile per User

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the new UserAdmin with UserProfile inline
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Include the UserProfileInline

admin.site.register(User, CustomUserAdmin)  # Register the User with the new admin


@admin.register(ExercisePlan)
class ExercisePlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'created_at') 
    search_fields = ('title',)  #  searchable fields

@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'calories', 'created_at')  
    search_fields = ('title',)  #  searchable fields

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'created_at')  
    search_fields = ('name', 'description')  #  searchable fields
    list_filter = ('is_spotlight',)  # Add filter option for spotlight products

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')  
    search_fields = ('product__name', 'user__username')  #  searchable fields

@admin.register(CommunityUpdate)
class CommunityUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'update_text', 'created_at')  
    search_fields = ('update_text',)  #  searchable fields

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')  
    search_fields = ('name',)  #  searchable fields

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  
    search_fields = ('user__username', 'product__name')  #  searchable fields

