from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from django.apps import AppConfig
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class FitnessConfig(AppConfig):
    name = 'fitness'

    def ready(self):
        # Import signals after the app is ready
        import fitness.signals



@receiver(post_save, sender='auth.User')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender='auth.User')
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
