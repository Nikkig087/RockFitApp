# Generated by Django 4.2.15 on 2024-12-22 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0013_remove_subscriptionplan_pause_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityupdate',
            name='content',
            field=models.TextField(default='No content'),
        ),
    ]
