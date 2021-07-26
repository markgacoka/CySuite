from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

def privacy_policy(request):
    return render(request, 'pages/privacy-policy.html')

def terms_conditions(request):
    return render(request, 'pages/terms-conditions.html')

def login(request):
    return render(request, 'auth/login.html')

def register(request):
    return render(request, 'auth/register.html')

def forgot_password(request):
    return render(request, 'auth/forgot-password.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def projects(request):
    return render(request, 'dashboard/projects.html')

def notes(request):
    return render(request, 'dashboard/notes.html')

def subdomain_enum(request):
    return render(request, 'dashboard/subdomain_enum.html')

def directory_enum(request):
    return render(request, 'dashboard/directory_enum.html')

def vuln_analysis(request):
    return render(request, 'dashboard/vuln_analysis.html')
    
def dorking(request):
    return render(request, 'dashboard/dorking.html')

def exploit(request):
    return render(request, 'dashboard/exploits.html')

def req_tamperer(request):
    return render(request, 'dashboard/req_tamperer.html')

def wordlist_gen(request):
    return render(request, 'dashboard/wordlist_gen.html')

def decoder(request):
    return render(request, 'dashboard/decoder.html')

def file_upload(request):
    return render(request, 'dashboard/file_upload.html')


def post(request):
    return render(request, 'posts/post1.html')
