from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomPasswordChangeForm

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user  # Show logged-in user's profile

class UserProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = CustomUserUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user  # Only update logged-in user's profile

class UserPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')
