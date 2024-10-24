from profile import Profile
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Post , Profile , Pet , Shelter
from django.contrib import messages
from django.db.models import Q
from .forms import CommentForm






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

        # Redirect to the success URL
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add error message when form is invalid
        messages.error(self.request, "There was an error in your registration. Please correct the errors below.")
        return super().form_invalid(form)

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


        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()


        profile = form.save(commit=False)
        profile.user = user
        profile.save()

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


class ShelterCreateView(CreateView):
    model = Shelter
    fields = ['name','description','contact_email','owner','phone_number','website','address']
    template_name = 'app/shelter_form.html'
    success_url = reverse_lazy('shelter_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ShelterUpdateView(UpdateView):
    model = Shelter
    fields = ['name','description','contact_email','owner','phone_number','website','address']
    template_name = 'app/shelter_edit.html'
    success_url = reverse_lazy('shelter_list')

class ShelterListView(ListView):
    model = Shelter
    context_object_name = 'shelters'
    template_name = 'app/shelter_list.html'

    def get_queryset(self):
        return Shelter.objects.filter(owner=self.request.user)

class ShelterDetailView(DetailView):
    model = Shelter
    template_name = 'app/shelter_detail.html'
    context_object_name = 'shelter'


class ShelterDeleteView(DeleteView):
    model = Shelter
    template_name = 'app/shelter_delete.html'
    success_url = reverse_lazy('shelter_list')


class PetCreateView(CreateView):
    model = Pet
    fields = ['name', 'animal','breed','age','description','post_image','visibility','owner','shelter']
    template_name = 'app/pet_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PetUpdateView(UpdateView):
    model = Pet
    fields = ['name', 'animal','breed','age','description','post_image','visibility','owner','shelter']

    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PetListView(ListView):
    model = Pet
    context_object_name = 'pets'
    template_name = 'app/pet_list.html'

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

class PetDetailView(DetailView):
    model = Pet
    template_name = 'app/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        # Ensure the pet belongs to the current user or is public
        return Pet.objects.filter(owner=self.request.user) | Pet.objects.filter(visibility='PUBLIC')

class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'app/pet_delete.html'
    success_url = reverse_lazy('pet_list')

