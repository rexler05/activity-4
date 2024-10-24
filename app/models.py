from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Shelter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contact_email = models.EmailField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)  # Link shelter to user
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('shelter_detail', kwargs={'pk': self.pk})


class Pet(models.Model):
    VISIBILITY_CHOICES = [
        ('EVERYONE', 'Everyone'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('FRIENDS', 'Friends')
    ]


    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    post_image = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='EVERYONE')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={'pk': self.pk})

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

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'