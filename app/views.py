from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pet, AdoptionApplication, Post, Comment, Notification
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

# Home Views
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

    def get_queryset(self):
        # Filter out pets that already have an owner
        return Pet.objects.filter(owner__isnull=True)

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet/pet_detail.html'
    context_object_name = 'pet'

class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image', 'is_adopted']
    template_name = 'pet/pet_create.html'
    success_url = reverse_lazy('pet_list')

class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image', 'is_adopted']
    template_name = 'pet/pet_update.html'
    success_url = reverse_lazy('pet_list')

class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pet/pet_delete.html'
    success_url = reverse_lazy('pet_list')

# AdoptionApplication Views
class AdoptionApplicationListView(LoginRequiredMixin, ListView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return AdoptionApplication.objects.filter(pet__owner__isnull=True)

class AdoptionApplicationDetailView(LoginRequiredMixin, DetailView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_detail.html'
    context_object_name = 'application'


class AdoptionApplicationCreateView(LoginRequiredMixin, CreateView):
    model = AdoptionApplication
    fields = ['pet', 'reason_for_adoption', 'additional_details']
    template_name = 'applicant/adoption_application_create.html'
    success_url = reverse_lazy('adoption_application_list')

    def get_form(self):
        form = super().get_form()
        # Filter out pets that are already adopted
        form.fields['pet'].queryset = Pet.objects.filter(is_adopted=False)
        return form

    def form_valid(self, form):
        # Save the adoption application and associate it with the current user
        form.instance.user = self.request.user
        application = form.save()

        # Create a notification for all admins
        admin_users = get_user_model().objects.filter(is_staff=True)

        for admin in admin_users:
            Notification.objects.create(
                user=admin,  # Notify the admin user
                application=application,  # Link the notification to the application
                message=f"A new adoption application has been submitted for the pet '{application.pet.name}'. Please review it."
                # Custom message
            )

        # Redirect after saving
        return super().form_valid(form)

class AdoptionApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = AdoptionApplication
    fields = ['pet', 'reason_for_adoption', 'additional_details', 'status']
    template_name = 'applicant/adoption_application_update.html'
    success_url = reverse_lazy('adoption_application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.get_object()  # Ensure `application` is passed
        return context

class AdoptionApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_delete.html'
    success_url = reverse_lazy('adoption_application_list')


class AdoptionApplicationApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff  # Only staff can approve applications

    def post(self, request, pk, *args, **kwargs):
        application = get_object_or_404(AdoptionApplication, pk=pk)
        pet = application.pet

        # Update the pet's owner and set it as adopted
        pet.owner = application.user
        pet.is_adopted = True
        pet.save()

        # Update application status
        application.status = "APPROVED"
        application.save()

        return redirect('adoption_application_list')

# Post Views
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories']
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories']
    template_name = 'news/post_update.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')

# Comment Views
class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    context_object_name = 'comments'

class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['post', 'body']
    template_name = 'comment/comment_form.html'
    success_url = reverse_lazy('comment_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'comment/comment_update.html'
    success_url = reverse_lazy('comment_list')

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    success_url = reverse_lazy('comment_list')

# Notification Views
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')

class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'notification/notification_detail.html'
    context_object_name = 'notification'

class NotificationCreateView(LoginRequiredMixin, CreateView):
    model = Notification
    fields = ['application', 'message', 'is_read']
    template_name = 'notification/notification_create.html'
    success_url = reverse_lazy('notification_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Notification
    fields = ['message', 'is_read']
    template_name = 'notification/notification_update.html'
    success_url = reverse_lazy('notification_list')

class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = 'notification/notification_delete.html'
    success_url = reverse_lazy('notification_list')
