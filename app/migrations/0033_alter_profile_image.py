# Generated by Django 5.1.1 on 2024-11-24 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to='profile_images/'),
        ),
    ]
