from django.db import models
from django.conf import settings
from django.urls import reverse




class Pet(models.Model):
    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField()
    post_image = models.ImageField(upload_to='pets/')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={'pk': self.pk})



class AdoptionApplication(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason_for_adoption = models.TextField()
    additional_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=
    [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')],
        default='PENDING'
    )

    def __str__(self):
        return f"Application by {self.user.username} for {self.pet}"  # ✅ Correct

    def get_absolute_url(self):
        return reverse('adoption_application_detail', kwargs={'pk': self.pk})





class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    post_image = models.ImageField(upload_to='media/', null=True, blank=True)
    post_categories = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.pk})

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message



    def get_absolute_url(self):
        return reverse('notification_detail', kwargs={'pk': self.pk})

