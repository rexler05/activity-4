from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment , AdoptionApplication





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