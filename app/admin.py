from django.contrib import admin
from .models import  Post, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'phone_number')

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Post)


