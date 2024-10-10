from django.urls import path
from .views import LoginPageView, HomePageView, AboutPageView, ContactPageView
from .import views

urlpatterns = [
    path('', LoginPageView, name='login'),
    path('join', views.join, name='join'),
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),

]