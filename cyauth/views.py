import os

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from cyauth.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, FeedbackForm, PasswordUpdateForm, ProfileUpdateForm
from main.forms import NewsletterForm
from .models import UserProfile
from .models import Account

def index(request):
    if request.user.is_authenticated == True:
        return redirect('dashboard')
    else:
        context = {}
        if request.POST:
            if request.POST['subscriber'] == '' or request.POST['subscriber'] == None:
                pass
            else:
                newsletter_form = NewsletterForm(request.POST)
                if newsletter_form.is_valid():
                    newsletter_form.save()
                return redirect('thank_you')
    return render(request, 'index.html', context)

def thank_you(request):
    if request.user.is_authenticated == True:
        return redirect('dashboard')
    else:
        return render(request, 'pages/thankyou.html')

def dashboard(request):
    if request.user.is_authenticated == True:
        context = {}
        context['profile_account'] = request.user.profile
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('index')
        
def reset_password(request):
    return render(request, 'auth/forgot-password.html')

def registration_view(request):
    context = {}
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('dashboard')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
    context['registration_form'] = form
    return render(request, 'auth/register.html', context)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
        
            if user:
                request.session['project'] = request.session.get('project', None)
                login(request, user)
                return redirect('dashboard')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'auth/login.html', context)


def logout_view(request):
    if 'project' in request.session:
        del request.session['project']
        request.session.modified = True
    logout(request)
    return redirect("index")

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    if request.method == 'POST':
        if 'feedback' in request.POST.keys():
            print(request.user.name)
            feedback_form = FeedbackForm(request.POST, instance=request.user)
            if feedback_form.is_valid():
                feedback_form.initial = {
                    "feedback": request.POST['feedback']
                }
                feedback_form.save()
                context['success_message'] = 'Feedback has been received!'
            else:
                context['error_message'] = 'An error occurred!'
            context['feedback_form'] = feedback_form
            context['profile_account'] = request.user.profile

        elif 'email' and 'username' in request.POST.keys():
            account_form = AccountUpdateForm(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username']
                }
                account_form.save()
                context['success_message'] = 'Updated'
            else:
                context['error_message'] = 'An error occurred!'
            context['account_form'] = account_form
            context['profile_account'] = request.user.profile

        elif 'old_password' in request.POST.keys():
            password_form = PasswordUpdateForm(request.POST, instance=request.user)
            if password_form.is_valid():
                password_form.save()
                context['success_message'] = 'Password Changed!'
                return redirect('login')
            else:
                context['profile_account'] = request.user.profile
                context['error_message'] = 'An error occurred!'
            context['password_form'] = password_form
        elif 'delete' in request.POST.keys():
            Account.objects.filter(username__iexact=request.user.username).delete()
            return redirect('index')
        elif len(request.FILES.get('image')) != 0:
            userprofile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if userprofile.is_valid():
                filename = request.FILES['image'].name
                if UserProfile.objects.get(username=request.user).image != 'default.jpg':
                    try:
                        os.remove(UserProfile.objects.get(username=request.user).image.path)
                    except:
                        print("Tried to remove a non-existent profile image")
                userprofile.save()
                context['success_message'] = 'Your profile has been updated!'
                context['profile_account'] = request.user.profile
        else:
            pass
    else:
        account_form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username
            }
        )
        context['account_form'] = account_form
        context['profile_account'] = request.user.profile
    return render(request, 'dashboard/profile.html', context)