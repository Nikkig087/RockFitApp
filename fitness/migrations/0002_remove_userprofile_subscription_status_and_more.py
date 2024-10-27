# Generated by Django 4.2.15 on 2024-10-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='subscription_status',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fitness_goal',
            field=models.CharField(blank=True, default='No goal set yet', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
