from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Post


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'

class BlogListView(ListView):
    model = Post
    template_name ='app/blog_list.html'
