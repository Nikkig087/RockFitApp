# Register your models here.
from django.contrib import admin
from .models import ExercisePlan, NutritionPlan, Product, Review, CommunityUpdate, SubscriptionPlan, Wishlist, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


'''
This module customizes the Django admin site for the models specified below
'''
class UserProfileInline(admin.StackedInline): 
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('name', 'email', 'profile_picture', 'fitness_goal', 'age', 'phone', 'subscription_status','subscription_plan')  # Add subscription_plan
    max_num = 1  


admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,) 

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
    list_display = ('name', 'price', 'duration')  
    search_fields = ('name',) 

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  
    search_fields = ('user__username', 'product__name')