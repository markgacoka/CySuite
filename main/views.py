from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

def login(request):
    return render(request, 'auth/login.html')

def register(request):
    return render(request, 'auth/register.html')

def forgot_password(request):
    return render(request, 'auth/forgot-password.html')
