from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms_conditions(request):
    return render(request, 'terms-conditions.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

def login(request):
    return render(request, 'auth/login.html')

def register(request):
    return render(request, 'auth/register.html')

def forgot_password(request):
    return render(request, 'auth/forgot-password.html')

def dashboard(request):
    return render(request, 'dashboard.html')
