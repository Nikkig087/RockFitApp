"""
Signals for automatically creating and saving UserProfile instances.

This module contains signal handlers that create and save UserProfile instances
whenever a User object is created or updated. The signals ensure that each user
has an associated profile.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

"""
    Signal handler to create a UserProfile when a new User is created.

    Args:
        sender (class): The model class that sent the signal (User).
        instance (User): The actual instance being saved.
        created (bool): Whether a new User instance was created.
        **kwargs: Additional keyword arguments.

    This function checks if a new User instance has been created, and if so,
    it creates an associated UserProfile instance.
"""


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


"""
    Signal handler to save the UserProfile when the User instance is saved.

    Args:
        sender (class): The model class that sent the signal (User).
        instance (User): The actual instance being saved.
        **kwargs: Additional keyword arguments.

    This function ensures that the associated UserProfile instance is saved
    whenever the User instance is updated.
"""


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
