from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import FailedPayment

@receiver(post_save, sender=FailedPayment)
def send_failed_payment_email(sender, instance, **kwargs):
    send_mail(
        'Payment Failed',
        f'Your payment of ${instance.amount} has failed. Please try again.',
        'noreply@example.com',
        [instance.email],
        fail_silently=False,
    )