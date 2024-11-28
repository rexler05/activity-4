from profile import Profile
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView , View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Post, Profile, Pet, AdoptionApplication ,Notification
from django.contrib import messages
from .forms import CommentForm





class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.get_or_create(
            user=user,
            age=form.cleaned_data['age'],
            gender=form.cleaned_data['gender'],
            phone_number=form.cleaned_data['phone_number']
        )
        login(self.request, user)
        messages.success(self.request, "Registration successful! You are now logged in.")
        return redirect('home')


class LoginPageView(FormView):
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
    template_name = 'app/profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)  # User posts
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
        return reverse_lazy('profile')

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

        profile = form.save(commit=False)
        profile.user = user

        image = form.cleaned_data.get('image')
        if image:
            profile.image = image
        else:
            profile.image = None

        profile.save()
        return super().form_valid(form)


# Logout View
class LogoutPageView(LogoutView):
    next_page = reverse_lazy('login')




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
        return Post.objects.all()


@method_decorator(login_required, name='dispatch')
class BlogDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/blog_detail.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)



@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories']
    template_name = 'app/blog_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'post_categories']
    template_name = 'app/blog_update.html'

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'app/blog_delete.html'
    success_url = reverse_lazy('blog')





@method_decorator(login_required, name='dispatch')
class PetCreateView(CreateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image']
    template_name = 'app/pet_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PetUpdateView(UpdateView):
    model = Pet
    fields = ['name', 'animal', 'breed', 'age', 'description', 'post_image']
    template_name = 'app/pet_update.html'

    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)


class PetListView(ListView):
    model = Pet
    context_object_name = 'pets'
    template_name = 'app/pet_list.html'

    def get_queryset(self):
        return Pet.objects.filter(is_adopted=False)

@method_decorator(login_required, name='dispatch')
class PetDetailView(DetailView):
    model = Pet
    template_name = 'app/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        return Pet.objects.filter(is_adopted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = self.get_object()
        context['applications'] = pet.adoptionapplication_set.all()  # Changed here
        return context


@method_decorator(login_required, name='dispatch')
class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'app/pet_delete.html'
    success_url = reverse_lazy('pets')

    def test_func(self):
        pet = self.get_object()
        return self.request.user.is_staff or pet.owner == self.request.user

    def get_object(self, queryset=None):
        return get_object_or_404(Pet, pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class AdoptionApplicationCreateView(CreateView):
    model = AdoptionApplication
    fields = ['reason_for_adoption', 'additional_details']
    template_name = 'app/adoption_application_create.html'

    def form_valid(self, form):
        pet = Pet.objects.get(pk=self.kwargs['pk'])
        form.instance.pet = pet
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = Pet.objects.get(pk=self.kwargs['pk'])
        context['pet'] = pet  # Make sure pet is in the context
        return context

    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class AdoptionApplicationDetailView(DetailView):
    model = AdoptionApplication
    template_name = 'app/adoption_application_detail.html'
    context_object_name = 'application'



@method_decorator(login_required, name='dispatch')
class AdoptionApplicationsListView(ListView):
    model = AdoptionApplication
    template_name = 'app/adoption_application.html'
    context_object_name = 'applications'


@method_decorator(login_required, name='dispatch')
class ApproveAdoptionView(View):
    def post(self, request, pk):
        application = get_object_or_404(AdoptionApplication, pk=pk)

        # Set the application status to approved
        application.status = 'APPROVED'
        application.save()

        # Update the pet's adoption status and owner
        pet = application.pet
        pet.is_adopted = True
        pet.owner = application.user  # Assign the approved adopter as the new owner
        pet.save()

        # Notify the user
        Notification.objects.create(
            user=application.user,
            application=application,
            message=f"Your adoption application for {application.pet.name} has been approved!, "
                    f"You can now go to our Pet Adoption Center for further process of adoption ,"
        )

        return redirect('adoption_application_detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class DenyAdoptionView(View):
    def post(self, request, pk):
        application = get_object_or_404(AdoptionApplication, pk=pk)
        application.status = 'DENIED'
        application.save()

        pet = application.pet
        pet.is_adopted = False
        pet.owner = None
        pet.save()

        Notification.objects.create(
            user=application.user,
            application=application,
            message=f"Your adoption application for {application.pet.name} has been denied!"
        )

        return redirect('adoption_application_detail', pk=pk)



@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    model = Notification
    template_name = 'app/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')





class MarkNotificationAsReadView(View):
    def post(self, request, pk, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return redirect('notification_list')

