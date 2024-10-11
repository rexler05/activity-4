from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from .forms import MemberForm
from django.contrib import messages
from .models import Member



def LoginPageView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:

            return render(request,'app/login.html', {'error': 'Invalid username or password'})
    return render(request, 'app/login.html')

def join(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your form has been submitted successfully.')
            return redirect('home')
        else:
            messages.error(request, ('There was an error with your submission.'))

            return render(request, 'app/join.html', {'form': MemberForm()})

    else:
        return render(request, 'app/join.html',{})


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'