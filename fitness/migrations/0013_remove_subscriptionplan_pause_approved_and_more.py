# Generated by Django 4.2.15 on 2024-12-16 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0012_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='pause_approved',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='pause_requested',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='paused_at',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='resume_approved',
        ),
        migrations.RemoveField(
            model_name='subscriptionplan',
            name='resume_requested',
        ),
    ]