from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from .forms import MemberForm
from django.contrib import messages
from .models import Member


def LoginPageView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwd']  # Ensure this matches the form input name
        member = authenticate(request, username=username, passwd=password)
        if member is not None:
            login(request, member)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authentication/login.html')

def join(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():

            member = form.save()

            username = request.POST['username']
            password = request.POST['passwd']

            user = Member.objects.filter(username=username, passwd=password).first()

            if user:
                request.session['user_id'] = user.id
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