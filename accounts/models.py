from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10,  choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default_profile.jpg')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

