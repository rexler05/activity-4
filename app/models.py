from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=100, null=True)
    passwd = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return self.fname + ' ' + self.lname