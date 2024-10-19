from django.urls import path
from .views import  HomePageView, AboutPageView, ContactPageView, BlogListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),


]