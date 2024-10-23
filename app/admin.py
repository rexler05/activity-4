from django.contrib import admin
from .models import  Post, Profile, Pet ,Shelter

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'phone_number')

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Post)

admin.site.register(Pet)

admin.site.register(Shelter)


