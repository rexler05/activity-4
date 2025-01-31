from django.urls import path
from .views import SignUp, UserProfileView, UserProfileUpdateView, UserPasswordChangeView

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),  # For viewing user profile
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),  # For updating user profile
    path('profile/change-password/', UserPasswordChangeView.as_view(), name='change_password'),

]