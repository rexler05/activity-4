from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pet, AdoptionApplication, Post, Comment, Notification
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'

# Pet Views
class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'pet/pet_list.html'
    context_object_name = 'pets'

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet/pet_detail.html'
    context_object_name = 'pet'

class PetCreateView(CreateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image', 'is_adopted']
    template_name = 'pet/pet_create.html'

class PetUpdateView(UpdateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image', 'is_adopted']
    template_name = 'pet/pet_update.html'

class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'pet/pet_delete.html'
    success_url = reverse_lazy('pet_list')

# AdoptionApplication Views
class AdoptionApplicationListView(LoginRequiredMixin, ListView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_list.html'
    context_object_name = 'applications'


class AdoptionApplicationDetailView(DetailView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_detail.html'
    context_object_name = 'application'

class AdoptionApplicationCreateView(CreateView):
    model = AdoptionApplication
    fields = ['pet', 'reason_for_adoption', 'additional_details']
    template_name = 'applicant/adoption_application_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adoption_application_list')





class AdoptionApplicationUpdateView(UpdateView):
    model = AdoptionApplication
    fields = ['pet', 'user', 'reason_for_adoption', 'additional_details', 'status']
    template_name = 'applicant/adoption_application_update.html'



class AdoptionApplicationDeleteView(DeleteView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_delete.html'
    success_url = reverse_lazy('adoption_application_list')







# Post Views
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories']
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')



class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories']
    template_name = 'news/post_update.html'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')

# Comment Views
class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    context_object_name = 'comments'

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment'

class CommentCreateView(CreateView):
    model = Comment
    fields = ['post', 'author', 'body']
    template_name = 'comment/comment_form.html'

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['post', 'author', 'body']
    template_name = 'comment/comment_update.html'

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('comment_list')

# Notification Views
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Filter notifications by the logged-in user
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')

class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notification/notification_detail.html'
    context_object_name = 'notification'

class NotificationCreateView(CreateView):
    model = Notification
    fields = ['user', 'application', 'message', 'is_read']
    template_name = 'notification/notification_create.html'

class NotificationUpdateView(UpdateView):
    model = Notification
    fields = ['user', 'application', 'message', 'is_read']
    template_name = 'notification/notification_update.html'

class NotificationDeleteView(DeleteView):
    model = Notification
    template_name = 'notification/notification_delete.html'
    success_url = reverse_lazy('notification_list')
