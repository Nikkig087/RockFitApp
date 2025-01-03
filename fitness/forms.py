"""
Forms for managing user profiles and reviews in the fitness application.

This module defines forms based on the UserProfile and Review models. These forms 
include custom initialization for CSS classes and validation logic to ensure data consistency.
"""
from django import forms
from .models import UserProfile, SubscriptionPlan, Review

from .models import NewsletterSubscription
from .models import ContactMessage

class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email to subscribe'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'email', 'profile_picture', 'fitness_goal', 'age', 'phone']
    
   
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.

        This method updates the widget attributes to add Bootstrap-compatible 
        CSS classes, ensuring a consistent and user-friendly appearance.
        """
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['fitness_goal'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})

    
    def clean_username(self):
        """
        Custom validation for the username field.

        Ensures that the username is between 5 and 150 characters long. 
        Raises a validation error if the criteria are not met.

        Returns:
            str: The validated username.

        Raises:
            forms.ValidationError: If the username is too short or too long.
        """
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        if len(username) > 150:
            raise forms.ValidationError("Username must not exceed 150 characters.")
        return username

class ReviewForm(forms.ModelForm):
    """
    Form for submitting product reviews.

    This form allows users to provide a rating and comment for products. 
    The comment field includes a custom widget for better usability.

    Attributes:
        Meta (class): Defines the model and fields included in the form.
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }


class UserProfileForm(forms.ModelForm):
    """
    Form for creating and updating user profiles (alternate version).

    This version of the form manages user information without the username field. 
    It includes custom CSS classes for styling each field.

    Attributes:
        Meta (class): Defines the model and fields included in the form.
    """
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'profile_picture', 'fitness_goal', 'age', 'phone']
    
   
    def __init__(self, *args, **kwargs):
        """
        Initializes the form with custom CSS classes for each field.

        This method updates the widget attributes to add Bootstrap-compatible 
        CSS classes, ensuring a consistent and user-friendly appearance.
        """
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['fitness_goal'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']




class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("This field is required.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'pause_requested', 'pause_approved', 'subscription_plan', 'paused_at']

    
    def clean(self):
        cleaned_data = super().clean()
        pause_requested = cleaned_data.get('pause_requested')
        pause_approved = cleaned_data.get('pause_approved')

        if pause_approved:
            cleaned_data['pause_requested'] = False 

        return cleaned_data