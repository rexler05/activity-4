from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse





class Pet(models.Model):
    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField()
    post_image = models.ImageField(upload_to='pets/')
    visibility = models.CharField(max_length=20, choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')])
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={'pk': self.pk})


class AdoptionEvent(models.Model):
    EVENT_CHOICES = [
        ('APPLICATION_SUBMITTED', 'Application Submitted'),
        ('APPLICATION_APPROVED', 'Application Approved'),
        ('APPLICATION_DENIED', 'Application Denied'),
        ('PET_ADOPTED', 'Pet Adopted'),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)  # To store additional info if needed

    def __str__(self):
        return f"{self.event_type} for {self.pet.name} by {self.user.username} on {self.timestamp}"


class AdoptionApplication(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason_for_adoption = models.TextField()
    additional_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')], default='PENDING')

    def __str__(self):
        return f"Application for {self.pet.name} by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1)
    phone_number = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


    def __str__(self):
        return str(self.user)

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
    post_image = models.ImageField(upload_to='media/', null=True, blank=True)
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
