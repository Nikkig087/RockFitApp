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
from django.contrib import admin
from .models import UserProfile
from django.utils.timezone import now


class UserProfileInline(admin.StackedInline):
    """
    Inline admin interface for associating UserProfile with User.

    This class allows the UserProfile to be edited directly within the User admin interface. It is not deletable
    to maintain the relationship between users and their profiles.

    Attributes:
        model (model): The UserProfile model associated with this inline.
        can_delete (bool): Determines if the UserProfile inline can be deleted. Default is False.
        verbose_name_plural (str): Custom label for the UserProfile inline section in the admin interface.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


def approve_pause(modeladmin, request, queryset):
    """
    Action to approve selected pause requests for UserProfiles.

    This function checks if the pause request is pending for each selected UserProfile, and if so,
    it approves the pause request, records the time it was approved, and updates the profile.

    Attributes:
        modeladmin (ModelAdmin): The ModelAdmin instance handling this action.
        request (HttpRequest): The request object containing details about the current session.
        queryset (QuerySet): The selected queryset of UserProfiles to act upon.
    """
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
    """
    Admin interface for managing UserProfile instances.

    This class handles the configuration of the UserProfile admin interface, including
    the ability to approve or reject pause requests, and modifying the list view.

    Attributes:
        form (form): The form used for editing UserProfiles.
        list_display (list): Fields to display in the UserProfile list view.
        list_filter (list): Fields to filter the UserProfiles by in the admin interface.
        actions (list): Actions to perform on selected UserProfiles in the list view.
    """
    form = UserProfileForm  

    list_display = ['user', 'pause_requested', 'pause_approved', 'subscription_plan']
    list_filter = ['pause_requested', 'pause_approved']
    
    actions = ['approve_pause', 'reject_pause']

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to handle pause approval logic.

        This method ensures that when a pause request is approved, the pause_requested flag is reset
        to false before saving the UserProfile.

        Attributes:
            request (HttpRequest): The request object containing session details.
            obj (Model instance): The UserProfile object being saved.
            form (Form instance): The form being used to save the model.
            change (bool): Flag indicating whether the model is being changed or created.
        """
        if obj.pause_approved:  
            obj.pause_requested = False
        super().save_model(request, obj, form, change)

    def approve_pause(self, request, queryset):
        """
        Approve the pause request for selected UserProfile instances.

        This method is intended to be used as an admin action to approve the pause request for one or more
        UserProfile instances selected in the Django admin interface. It will mark the `pause_requested` field as
        False, approve the `pause_approved` field, and set the time when the pause was approved in the `paused_at` field.

        If a UserProfile does not have a pending pause request, a message will be displayed indicating that no request
        is available for approval.

        Args:
        request (HttpRequest): The HTTP request object, used to send messages to the admin interface.
        queryset (QuerySet): A QuerySet of selected UserProfile instances to which the action will be applied.

        Notes:
        - This method uses `timezone.now()` to record the exact time when the pause request is approved.
        - The `pause_requested` field is automatically set to False when the request is approved.
        - The action is visible as "Approve selected pause requests" in the Django admin interface.

    """        
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
        """
        Reject the selected pause requests.

        This action sets both the pause_requested and pause_approved flags to False for the selected
        UserProfiles.

        Attributes:
            request (HttpRequest): The request object containing session details.
            queryset (QuerySet): The selected queryset of UserProfiles to reject the pause request for.
        """
        queryset.update(pause_approved=False, pause_requested=False)
        self.message_user(request, "Pause request rejected.")

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the User model.

    This class extends the default Django UserAdmin to include the UserProfile inline within the
    User admin interface. This allows editing of the UserProfile directly from the User's admin page.

    Attributes:
        inlines (tuple): The list of inline admin classes to display in the User admin form.
    """
    inlines = (UserProfileInline,) 


admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin)  


@admin.register(ExercisePlan)
class ExercisePlanAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ExercisePlan instances.

    This class configures the admin interface for the ExercisePlan model, including the fields
    to display in the list view and the ability to search by the title.

    Attributes:
        list_display (tuple): Fields to display in the ExercisePlan list view.
        search_fields (tuple): Fields to search by in the ExercisePlan admin interface.
    """
    list_display = ('title', 'duration', 'created_at')
    search_fields = ('title',)

#@admin.register(NutritionPlan)
#class NutritionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for managing NutritionPlan instances.

    This class configures the admin interface for the NutritionPlan model, including the fields
    to display in the list view and the ability to search by the title.

    Attributes:
        list_display (tuple): Fields to display in the NutritionPlan list view.
        search_fields (tuple): Fields to search by in the NutritionPlan admin interface.
    """
 #   list_display = ('title', 'calories', 'created_at')
  #  search_fields = ('title',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Product instances.

    This class configures the admin interface for the Product model, including the fields
    to display, search, and filter by in the admin view.

    Attributes:
        list_display (tuple): Fields to display in the Product list view.
        search_fields (tuple): Fields to search by in the Product admin interface.
        list_filter (tuple): Fields to filter products by in the admin view.
    """
    list_display = ('name', 'price', 'stock_quantity', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_spotlight',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Review instances.

    This class configures the admin interface for the Review model, including displaying fields,
    filtering by approval status and creation date, and allowing search by user and product.

    Attributes:
        list_display (tuple): Fields to display in the Review list view.
        list_filter (tuple): Fields to filter reviews by in the admin view.
        search_fields (tuple): Fields to search by in the Review admin interface.
    """
    list_display = ('user', 'product', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')


@admin.register(CommunityUpdate)
class CommunityUpdateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing CommunityUpdate instances.

    This class configures the admin interface for the CommunityUpdate model, including displaying
    the update text and user, as well as providing search functionality for the update text.

    Attributes:
        list_display (tuple): Fields to display in the CommunityUpdate list view.
        search_fields (tuple): Fields to search by in the CommunityUpdate admin interface.
    """
    list_display = ('user', 'update_text', 'created_at')
    search_fields = ('update_text',)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for managing SubscriptionPlan instances.

    This class configures the admin interface for the SubscriptionPlan model, including fields
    to display in the list view, filtering by active status and spotlight feature, and search functionality.

    Attributes:
        list_display (tuple): Fields to display in the SubscriptionPlan list view.
        list_filter (tuple): Fields to filter SubscriptionPlans by in the admin view.
        search_fields (tuple): Fields to search by in the SubscriptionPlan admin interface.
        fields (tuple): Fields to include in the form for creating/editing SubscriptionPlans.
    """
    list_display = ('name', 'price', 'is_active', 'is_spotlight')
    list_filter = ('is_active', 'is_spotlight')
    search_fields = ('name',)

  
    fields = ('name', 'price', 'duration', 'benefits', 'is_active', 'is_spotlight')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a UserProfile when a User is saved.

    This function is triggered after a User instance is saved. If the User is newly created,
    it automatically creates a corresponding UserProfile. If the User is updated, it ensures
    that the associated UserProfile is also saved (i.e., any changes made to the User will be reflected
    in the UserProfile).

    Args:
        sender (Model): The model that sent the signal (User).
        instance (Model instance): The User instance being saved.
        created (bool): A flag indicating whether the User instance was newly created (True) or updated (False).
        kwargs (dict): Additional arguments passed to the signal, such as the request.

    Notes:
        - This signal ensures that every User instance has an associated UserProfile.
        - It does not create a new profile if the User already has an associated UserProfile.
    """
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

