from django import forms
from .models import UserProfile, SubscriptionPlan

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'fitness_goal', 'name', 'email', 'age', 'phone'] 
        widgets = {
            'subscription_plan': forms.Select()  # Dropdown selection for subscription plans
        }
