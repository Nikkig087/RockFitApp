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
from django.apps import AppConfig

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
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    def save_user_profile(sender, instance, **kwargs):
        """
    Signal handler to save the UserProfile when the User instance is saved.

    Args:
        sender (class): The model class that sent the signal (User).
        instance (User): The actual instance being saved.
        **kwargs: Additional keyword arguments.

    This function ensures that the associated UserProfile instance is saved
    whenever the User instance is updated.
    """
        #instance.userpro
        instance.userprofile.save()


#class FitnessConfig(AppConfig):
"""
    Configuration class for the 'fitness' application.

    This class is used to configure the fitness app and ensures that signals
    are imported and registered when the application is ready.
    """
name = 'fitness'

def ready(self):
         """
        Imports the signals module to register signal handlers.

        This method is called when the application is ready. Importing the signals
        here ensures that the signal handlers are connected and active.
        """
import fitness.signals


"""
Alternative signal handler to create a UserProfile when a new User is created.

    Args:
        sender (str): The model class that sent the signal ('auth.User').
        instance (User): The actual instance being saved.
        created (bool): Whether a new User instance was created.
        **kwargs: Additional keyword arguments.

    This function performs the same task as the earlier create_user_profile function,
    ensuring that a UserProfile is created for new User instances.
""
@receiver(post_save, sender='auth.User')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender='auth.User')
def save_user_profile(sender, instance, **kwargs):
    """
  #  Alternative signal handler to save the UserProfile when the User instance is saved.
#
 #   Args:
  #      sender (str): The model class that sent the signal ('auth.User').
   #     instance (User): The actual instance being saved.
    #    **kwargs: Additional keyword arguments.
#
#    This function performs the same task as the earlier save_user_profile function,
 #   ensuring that the UserProfile is saved whenever the User instance is updated.

#    instance.userprofile.save()
