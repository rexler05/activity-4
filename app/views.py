from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pet, AdoptionApplication, Post, Comment, Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .forms import CommentCreateForm

User = get_user_model()  # This gets the custom user model




class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'



# ---------------------- PET VIEWS ---------------------- #
class PetListView(ListView):
    model = Pet
    template_name = 'pet/pet_list.html'
    context_object_name = 'pets'

    def get_queryset(self):
        # Filter out pets that are already owned (owner is not null)
        return Pet.objects.filter(owner__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for pet in context['pets']:
            # Check if the user has already applied for adoption for this pet
            existing_application = AdoptionApplication.objects.filter(user=self.request.user, pet=pet).first()
            pet.already_applied = existing_application and existing_application.status in ['Pending', 'Approved']
        return context

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet/pet_detail.html'
    context_object_name = 'pet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = context['pet']

        # Check if the user has already applied for adoption for this pet
        existing_application = AdoptionApplication.objects.filter(user=self.request.user, pet=pet).first()
        context['already_applied'] = existing_application and existing_application.status in ['Pending', 'Approved']

        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    template_name = 'pet/pet_create.html'
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image']

    def form_valid(self, form):
        # Set the pet's owner to None, making it available for adoption
        form.instance.owner = None
        return super().form_valid(form)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    template_name = 'pet/pet_update.html'
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image']


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pet/pet_delete.html'
    success_url = reverse_lazy('pet_list')


class AdoptionApplicationListView(ListView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        """Return applications based on user role."""
        if self.request.user.is_staff:
            return AdoptionApplication.objects.all()
        return AdoptionApplication.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add pending and approved applications to context."""
        context = super().get_context_data(**kwargs)
        applications = self.get_queryset()

        # Ensure that approved applications are properly passed
        context['pending_applications'] = applications.filter(status__iexact='PENDING')
        context['approved_applications'] = applications.filter(status__iexact='APPROVED')

        return context


class AdoptionApplicationDetailView(DetailView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_detail.html'
    context_object_name = 'application'


class AdoptionApplicationCreateView(LoginRequiredMixin, CreateView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_create.html'
    fields = ['reason_for_adoption', 'additional_details']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_id = self.kwargs.get('pet_pk')
        pet = get_object_or_404(Pet, pk=pet_id)

        context['pet'] = pet

        # Check how many applications exist for this pet
        pet_applications_count = AdoptionApplication.objects.filter(pet=pet).count()
        context['pet_applications_count'] = pet_applications_count

        # Allow up to 3 applications for each pet
        max_applications_per_pet = 3
        context['application_limit_reached'] = pet_applications_count >= max_applications_per_pet

        return context

    def form_valid(self, form):
        pet_id = self.kwargs.get('pet_pk')
        pet = get_object_or_404(Pet, pk=pet_id)

        # Limit check for pet: Only allow a maximum of 3 applications for this pet
        max_applications_per_pet = 5
        pet_applications_count = AdoptionApplication.objects.filter(pet=pet).count()
        if pet_applications_count >= max_applications_per_pet:
            form.add_error(None, "This pet has already received the maximum number of adoption applications (3).")
            return self.form_invalid(form)

        # Assign user and pet to application
        form.instance.user = self.request.user
        form.instance.pet = pet
        response = super().form_valid(form)

        # Notify Admin
        self.notify_admin(pet, form.instance)

        return response

    def notify_admin(self, pet, application):
        """Send notification and email to all admin users."""
        admin_users = User.objects.filter(is_staff=True)  # Get all admin users

        # Create a notification for each admin
        for admin in admin_users:
            Notification.objects.create(
                recipient=admin,
                sender=self.request.user,
                application=application,
                message=f"A new adoption application has been submitted for {pet.name}.",
                notification_type="New Application"
            )

        # Optional: Send an email notification
        admin_emails = [admin.email for admin in admin_users if admin.email]
        if admin_emails:
            send_mail(
                subject=f"New Adoption Application for {pet.name}",
                message=f"A new adoption application has been submitted by {self.request.user.username} for {pet.name}.",
                from_email="your_email@example.com",
                recipient_list=admin_emails,
                fail_silently=True,
            )

    def get_success_url(self):
        return reverse_lazy('adoption_application_list')


class AdoptionApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_update.html'
    fields = ['reason_for_adoption', 'additional_details']

    def get_object(self, queryset=None):
        # Ensure we are getting the correct application instance
        return get_object_or_404(AdoptionApplication, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = self.get_object()
        context['application'] = application  # Pass the application to the context
        context['pet'] = application.pet  # Get the pet associated with the application
        return context

    def form_valid(self, form):
        # Ensure the user is assigned correctly (if you want to keep this functionality)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # After updating, redirect to the application detail page
        return reverse_lazy('adoption_application_detail', kwargs={'pk': self.kwargs['pk']})



class AdoptionApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_delete.html'
    success_url = reverse_lazy('adoption_application_list')


class AdoptionApplicationApproveView(LoginRequiredMixin, UpdateView):
    model = AdoptionApplication
    fields = []  # No need for any fields in the form
    template_name = 'applicant/adoption_application_approve.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AdoptionApplication, pk=self.kwargs['pk'])

    def form_valid(self, form):
        application = form.save(commit=False)
        pet = application.pet

        # Change pet status
        pet.is_adopted = True
        pet.owner = application.user
        pet.save()

        # Update application status
        application.status = 'Approved'
        application.save()

        # Send Notification to Applicant
        Notification.objects.create(
            sender=self.request.user,  # Admin approving the application
            recipient=application.user,  # The applicant
            application=application,
            message=f"Your adoption application for {pet.name} has been approved!",
            notification_type="APPROVAL"
        )

        messages.success(self.request, f"Adoption approved! Notification sent to {application.user.username}.")

        return redirect('adoption_application_list')  # Redirect to application list


class AdoptionApplicationRejectView(DeleteView):
    model = AdoptionApplication
    template_name = 'applicant/adoption_application_reject.html'
    context_object_name = 'application'
    success_url = reverse_lazy('adoption_application_list')  # Redirect to the application list after rejection

    def get_object(self, queryset=None):
        return get_object_or_404(AdoptionApplication, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Get the adoption application object
        application = self.get_object()

        # Get the pet associated with the application
        pet = application.pet

        # Update the application status to "Rejected"
        application.status = 'Rejected'
        application.save()

        # Provide a success message to the admin
        messages.success(request, f"The adoption application for {pet.name} has been rejected and deleted.")

        # Proceed with the deletion of the adoption application object
        return super().delete(request, *args, **kwargs)




# ---------------------- POST VIEWS ---------------------- #

class PostListView(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object  # The post instance

        # Add the comment form to the context if the user is authenticated
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentCreateForm(initial={'post': post})

        # Fetch comments related to this post
        context['comments'] = post.comment_set.all()  # This directly fetches comments related to the post

        return context

    def post(self, request, *args, **kwargs):
        # Handle the comment submission here
        post = self.get_object()  # Get the post based on the URL
        comment_form = CommentCreateForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirect back to the post detail page

        # If the form is invalid, re-render the page with form errors
        return self.render_to_response(self.get_context_data(comment_form=comment_form))

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    fields = ['title', 'body', 'post_image', 'post_categories']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/post_update.html'
    fields = ['title', 'body', 'post_image', 'post_categories']


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')


# ---------------------- COMMENT VIEWS ---------------------- #



class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'comment/comment_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_pk']})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comment/comment_update.html'
    fields = ['body']

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        )

class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'notification/notification_detail.html'
    context_object_name = 'notification'

class NotificationCreateView(LoginRequiredMixin, CreateView):
    model = Notification
    template_name = 'notification/notification_create.html'
    fields = ['recipient', 'application', 'message', 'notification_type']

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = 'notification/notification_delete.html'
    success_url = reverse_lazy('notification_list')

class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Notification
    template_name = 'notification/notification_update.html'
    fields = ['recipient', 'application', 'message', 'notification_type']
    success_url = reverse_lazy('notification_list')



