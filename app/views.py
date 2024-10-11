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
        form = MemberForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            age = request.POST['age']
            email = request.POST['email']
            passwd = request.POST['passwd']

            messages.success(request, ('There was an error'))
            #return redirect('join')
            return render(request, 'app/join.html',{'fname':fname,
                                                    'lname':lname,
                                                    'age':age,
                                                    'email':email,
                                                    'passwd':passwd})

        messages.success(request, ('Your Form has Been Submitted'))
        return redirect('home')

    else:
        return render(request, 'app/join.html',{})


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'