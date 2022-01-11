import os

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from cyauth.forms import AdditionalInfoForm, RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, FeedbackForm, PasswordUpdateForm
from rest_framework.authtoken.models import Token
from main.forms import NewsletterForm
from main.models import Newsletter
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

def additional_info_view(request):
    context = {}

    additional_form = AdditionalInfoForm(request.POST or None)
    if request.method == "POST":
        if additional_form.is_valid():
            curr_user_id = request.session['temp_user']
            curr_user = Account.objects.get(user_id=curr_user_id)
            company = additional_form.cleaned_data.get('company')
            role = additional_form.cleaned_data.get('role')
            password = additional_form.cleaned_data.get('password')
            curr_user.set_password(password)
            curr_user.company = company
            curr_user.role = role
            curr_user.save()
            curr_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, curr_user)
            if 'temp_user' in request.session:
                del request.session['temp_user']
        return redirect('dashboard')
    return render(request, 'auth/set_password.html', context)

def thank_you(request):
    if request.user.is_authenticated == True:
        return redirect('dashboard')
    else:
        return render(request, 'pages/thankyou.html')
        
def reset_password(request):
    return render(request, 'auth/forgot-password.html')

def registration_view(request):
    context = {}
    previous_input = {'first_name':'', 'last_name': '', 'email': '', 'username': '', 'company': '', 'role': ''}
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            request.session['project'] = request.session.get('project', None)
            request.session['sub_index'] = request.session.get('sub_index', 0)
            request.session['curr_subdomain'] = request.session.get('curr_subdomain', None)
            account.social_provider = 'Email'
            account.is_repo_linked = False
            account.api_token = Token.objects.get(user_id=account.user_id).key
            account.save()
            request.session.modified = True
            login(request, account)
            return redirect('dashboard')
        else:
            previous_input = {'first_name': request.POST.get('first_name'), 'last_name': request.POST.get('last_name'), 'email': request.POST.get('email'), 'username': request.POST.get('username'), 'company': request.POST.get('company'), 'role': request.POST.get('role')}
            context['registration_form'] = form
    else:
        form = RegistrationForm()
    context['registration_form'] = form
    context['previous_input'] = previous_input
    return render(request, 'auth/register.html', context)

def login_view(request):
    context = {}
    previous_input = {'email':'', 'password': ''}
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if (user.social_provider == 'Google' or user.social_provider == 'Github' or user.social_provider == 'Gitlab') and user.has_usable_password() == False:
                return render(request, 'auth/set_password.html', context)
            if user:
                request.session['project'] = request.session.get('project', None)
                request.session['sub_index'] = request.session.get('sub_index', 0)
                request.session['curr_subdomain'] = request.session.get('curr_subdomain', None)
                request.session.modified = True
                login(request, user)
                return redirect('dashboard')
        else:
            previous_input = {"email": request.POST.get('email'), "password": request.POST.get('password')}
    else:
        form = AccountAuthenticationForm()
    
    context['previous_input'] = previous_input
    context['login_form'] = form
    return render(request, 'auth/login.html', context)


def logout_view(request):
    if 'project' in request.session:
        request.session.clear()
        request.session.modified = True
    logout(request)
    return redirect("index")

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    if request.method == 'POST':
        if 'feedback' in request.POST.keys():
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

        elif 'email' and 'username' and 'company' and 'role' in request.POST.keys():
            account_form = AccountUpdateForm(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
                    "company": request.POST['role'],
                    "role": request.POST['role'],
                }
                account_form.save()
                context['success_message'] = 'Updated'
            else:
                context['error_message'] = 'An error occurred!'
            context['account_form'] = account_form

        elif 'old_password' in request.POST.keys():
            password_form = PasswordUpdateForm(request.POST, instance=request.user)
            if password_form.is_valid():
                password_form.save()
                context['success_message'] = 'Password Changed!'
                return redirect('login')
            else:
                context['error_message'] = 'An error occurred!'
            context['password_form'] = password_form
        elif 'delete' in request.POST.keys():
            Account.objects.filter(username__iexact=request.user.username).delete()
            Newsletter.objects.filter(subscriber__iexact=request.user.email).delete()
            request.session.clear()
            return redirect('index')
        elif len(request.FILES.get('image')) != 0:
            extension = str(request.FILES['image'].name.rsplit(".", 1)[-1])
            full_extension = str(request.user.user_id) + '.' + extension

            import boto3
            from dotenv import load_dotenv
            load_dotenv()

            s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key= os.environ.get('AWS_SECRET_ACCESS_KEY'))
            bucket = s3.Bucket(name="cysuite-bucket")
            image = request.FILES['image']
            image.name = full_extension
            bucket.upload_fileobj(image, 'media/profiles/' + full_extension)
            userprofile = Account.objects.get(user_id=request.user.user_id)
            userprofile.image = full_extension
            userprofile.save()
            context['success_message'] = 'Your profile has been updated!'
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
    return render(request, 'dashboard/profile.html', context)