# Generated by Django 4.2.15 on 2024-12-14 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0010_remove_userprofile_subscription_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]