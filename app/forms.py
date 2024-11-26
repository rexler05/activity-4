from django import forms
from django.forms import RadioSelect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Comment , AdoptionApplication


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=RadioSelect,  # Use RadioSelect widget here
        required=True
    )
    phone_number = forms.CharField(max_length=15, required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'age', 'gender', 'phone_number', 'password1', 'password2', 'image']  # Include image in fields


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(label="Email Address")
    age = forms.IntegerField(min_value=18, required=True, label="Age")
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=RadioSelect,  # Use RadioSelect widget here
        required=True
    )
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    image = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'gender', 'phone_number', 'image']

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment here...'}),
        }

class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ['reason_for_adoption', 'additional_details']

        widgets = {
            'reason_for_adoption': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Why do you want to adopt this pet?'}),
            'additional_details': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any additional details or requests...'}),
        }