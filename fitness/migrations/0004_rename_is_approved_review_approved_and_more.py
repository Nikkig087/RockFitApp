# Generated by Django 4.2.15 on 2024-12-04 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_alter_wishlist_unique_together_review_is_approved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='is_approved',
            new_name='approved',
        ),
        migrations.RemoveField(
            model_name='review',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(),
        ),
    ]