from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from .forms import MemberForm
from django.contrib import messages





def LoginPageView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:

            return render(request,'authentication/login.html', {'error': 'Invalid username or password'})
    return render(request, 'authentication/login.html')

def join(request):
    if request.method == "POST":
        form = MemberForm(request.POST or None)
        if form.is_valid():
            # Save the new member
            form.save()

            # Get the username and password to authenticate the new member
            username = request.POST['username']
            password = request.POST['passwd']

            # Authenticate the new member
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the new member
                login(request, user)
                messages.success(request, 'Your account has been created and you are now logged in.')
                return redirect('home')
            else:
                messages.error(request, 'There was a problem logging you in after sign-up.')
                return redirect('login')
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            age = request.POST['age']
            email = request.POST['email']
            passwd = request.POST['passwd']

            messages.error(request, 'There was an error in your form.')
            return render(request, 'app/join.html', {
                'fname': fname,
                'lname': lname,
                'age': age,
                'email': email,
                'passwd': passwd
            })
    else:
        return render(request, 'app/join.html', {})


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'