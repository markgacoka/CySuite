from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from cyauth.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

def index(request):
    if request.user.is_authenticated == True:
        return redirect('dashboard')
    else:
        return render(request, 'index.html')

def dashboard(request):
    if request.user.is_authenticated == True:
        return render(request, 'dashboard/dashboard.html')
    else:
        return redirect('index')
        
def reset_password(request):
    return render(request, 'auth/forgot-password.html')

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
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
                login(request, user)
                return redirect('dashboard')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    return redirect("index")

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username']
            }
            form.save()
            context['success_message'] = 'Updated'
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username
            }
        )
    context['account_form'] = form
    return render(request, 'dashboard/profile.html', context)
