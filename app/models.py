from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('EVERYONE', 'Everyone'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('FRIENDS', 'Friends')
    ]

    title = models.CharField(max_length=100)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    post_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    post_categories = models.CharField(max_length=100)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='EVERYONE')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={'pk': self.pk})