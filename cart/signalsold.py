from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Order Confirmation - Rockfit"
        message = f"Thank you for your order, {instance.full_name}! Your payment was successful."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender=Order)
def send_payment_failed_email(sender, instance, created, **kwargs):
    if not created:
        subject = "Payment Failed - Rockfit"
        message = f"Dear {instance.full_name},\n\nYour payment was unsuccessful. Please try again."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
