from profile import Profile
from django.urls import reverse
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView , View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Post, Profile, Pet, AdoptionEvent, AdoptionApplication
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .forms import CommentForm ,AdoptionApplicationForm

class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Save the user
        user = form.save()

        # Create a related profile
        Profile.objects.get_or_create(
            user=user,
            age=form.cleaned_data['age'],
            gender=form.cleaned_data['gender'],
            phone_number=form.cleaned_data['phone_number'],
            middle_name=form.cleaned_data['middle_name']
        )

        # Log the user in
        login(self.request, user)

        # Add success message
        messages.success(self.request, "Registration successful! You are now logged in.")

        # Redirect to profile creation page
        return redirect('create_profile')  # Adjust to your profile creation view URL


# Login View
class LoginView(FormView):
    template_name = 'app/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    model = Profile
    template_name = 'app/account_settings.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class ProfilePageView(DetailView):
    model = Profile
    template_name = 'app/profile.html'  # Create this template

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)  # Fetch user's posts
        return context


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'app/edit_profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        return initial

    def get_success_url(self):
        return reverse_lazy('account_settings')

    def form_valid(self, form):
        user = self.request.user

        # Update user details
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

        profile = form.save(commit=False)
        profile.user = user

        # Handle image separately in case no new image is uploaded
        if 'image' in form.cleaned_data and form.cleaned_data['image']:
            profile.image = form.cleaned_data['image']

        profile.save()  # Save the profile including the image if updated

        return super().form_valid(form)

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'app/home.html')



class HomePageView(ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'app/home.html'

    def get_queryset(self):

        return Profile.objects.all()

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'

class BlogListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/blog_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Show posts visible to everyone, public posts, and private/friends if the user is the author
            return Post.objects.filter(
                Q(visibility='EVERYONE') |
                Q(visibility='PUBLIC') |
                Q(visibility='PRIVATE', author=user) |
                Q(visibility='FRIENDS', author=user)
            ).distinct()
        else:
            # Only show posts visible to everyone and public posts for non-authenticated users
            return Post.objects.filter(
                Q(visibility='EVERYONE') |
                Q(visibility='PUBLIC')
            ).distinct()

class BlogDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/blog_detail.html'

    def get_queryset(self):
        user = self.request.user
        post = super().get_queryset()
        if user.is_authenticated:
            return post.filter(
                Q(visibility='EVERYONE') |
                Q(visibility='PUBLIC') |
                Q(visibility='PRIVATE', author=user) |
                Q(visibility='FRIENDS', author=user)
            )
        else:
            return post.filter(Q(visibility='EVERYONE') | Q(visibility='PUBLIC'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Fetch all comments related to the post
        context['comment_form'] = CommentForm()  # Add comment form to the context
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.get_object())

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)




class BlogCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories', 'visibility']
    template_name = 'app/blog_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories', 'visibility']

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'app/blog_delete.html'
    success_url = reverse_lazy('blog')




class OwnerAssignmentMixin:
    def assign_owner(self, form):
        if form.cleaned_data['visibility'] == 'PUBLIC':
            form.instance.owner = None  # Set owner to None for public pets
        else:
            form.instance.owner = self.request.user  # Set owner to the current user for private pets

class PetCreateView(OwnerAssignmentMixin, CreateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image', 'visibility']
    template_name = 'app/pet_form.html'

    def form_valid(self, form):
        self.assign_owner(form)
        return super().form_valid(form)

class PetUpdateView(OwnerAssignmentMixin, UpdateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image', 'visibility']
    template_name = 'app/pet_edit.html'

    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.assign_owner(form)
        return super().form_valid(form)

class PetListView(ListView):
    model = Pet
    context_object_name = 'pets'
    template_name = 'app/pet_list.html'

    def get_queryset(self):
        # Include pets that are public and not adopted
        return Pet.objects.filter(visibility='PUBLIC', is_adopted=False)

class PetDetailView(DetailView):
    model = Pet
    template_name = 'app/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        return Pet.objects.filter(is_adopted=False)

class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'app/pet_delete.html'
    success_url = reverse_lazy('pet_list')

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)



class AdoptionApplicationCreateView(CreateView):
    model = AdoptionApplication
    form_class = AdoptionApplicationForm
    template_name = 'app/adoption_application_form.html'
    success_url = reverse_lazy('pet_list')  # Redirect after successful submission

    def form_valid(self, form):
        pet_id = self.kwargs['pk']
        pet = get_object_or_404(Pet, pk=pet_id)
        form.instance.pet = pet  # Associate the pet with the application
        form.instance.user = self.request.user  # Associate the logged-in user with the application
        return super().form_valid(form)


class AdoptionApplicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AdoptionApplication
    template_name = 'app/adoption_application.html'
    context_object_name = 'applications'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return AdoptionApplication.objects.all()  # Adjust as needed for filtering

class AdoptionApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = AdoptionApplication
    template_name = 'app/adoption_application_detail.html'
    context_object_name = 'application'

    def test_func(self):
        return self.request.user.is_staff

class AdoptionApplicationApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(AdoptionApplication, pk=pk)

        # Update pet status to adopted
        application.pet.is_adopted = True
        application.pet.save()

        # Update application status to approved
        application.status = 'APPROVED'
        application.save()

        # Record the event
        AdoptionEvent.objects.create(
            event_type='APPLICATION_APPROVED',
            pet=application.pet,
            user=request.user,
            details={'reason': application.reason_for_adoption},
        )

        messages.success(request, f"Application for {application.pet.name} has been approved.")
        return redirect('adoption')

    def test_func(self):
        return self.request.user.is_staff

class AdoptionApplicationDenyView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(AdoptionApplication, pk=pk)

        # Update application status to denied
        application.status = 'DENIED'
        application.save()

        # Record the event
        AdoptionEvent.objects.create(
            event_type='APPLICATION_DENIED',
            pet=application.pet,
            user=request.user,
            details={'reason': application.reason_for_adoption},
        )

        messages.success(request, f"Application for {application.pet.name} has been denied.")
        return redirect('adoption')

    def test_func(self):
        return self.request.user.is_staff

class PetEventHistoryView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Pet  # Assuming you want to fetch events related to the Pet model
    template_name = 'app/adoption_transaction.html'
    context_object_name = 'pet'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = AdoptionEvent.objects.filter(pet=self.object)  # Adjust to fit your model
        return context

    def get_object(self, queryset=None):
        pet_id = self.kwargs.get('pet_id')
        return self.get_queryset().get(id=pet_id)  # Fetch the pet object using pet_id

class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, event_id):
        event = get_object_or_404(AdoptionEvent, id=event_id)  # Get the specific event
        return render(request, 'app/event_detail.html', {'event': event})  # Pass the event to the template

    def test_func(self):
        return self.request.user.is_staff