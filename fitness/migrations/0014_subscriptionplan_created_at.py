# Generated by Django 4.2.15 on 2024-11-27 16:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0013_subscriptionplan_is_spotlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]