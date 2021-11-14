from cyauth.models import UserProfile
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings

class MyLoginAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            return settings.LOGIN_REDIRECT_URL.format(
                id=request.user.user_id)

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        pass

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    created = False
    user = get_user_model()
    email_address = sociallogin.account.extra_data['email']

    if sociallogin.account.provider == 'twitter':
        name = sociallogin.account.extra_data['name'].split()
        username = sociallogin.account.extra_data['screen_name']
        if len(name) == 2:
            last_name = name[1]
        else:
            last_name = ''

        if not user.objects.filter(email=email_address).exists() and not user.objects.filter(username=username).exists():
            new_user, created = user.objects.update_or_create(
                username = username,
                email = email_address,
                is_admin = False,
                is_premium = False, 
                defaults = {
                    'first_name': name[0],
                    'last_name': last_name
                }
            )
            # verified = sociallogin.account.extra_data['verified']
        else:
            if user.objects.filter(email=email_address).exists():
                curr_user = user.objects.filter(email=email_address)
                perform_login(request, curr_user[0], email_verification='optional')

    if sociallogin.account.provider == 'facebook':
        username = sociallogin.account.extra_data['name']
        if not user.objects.filter(email=email_address).exists() and not user.objects.filter(username=username).exists():
            new_user, created = user.objects.update_or_create(
                email = email_address,
                username = username,
                is_admin = False,
                is_premium = False,
                defaults = {
                    'first_name': sociallogin.account.extra_data['first_name'],
                    'last_name': sociallogin.account.extra_data['last_name']
                }
            )
            # verified = sociallogin.account.extra_data['verified']
        else:
            if user.objects.filter(email=email_address).exists():
                curr_user = user.objects.filter(email=email_address)
                perform_login(request, curr_user[0], email_verification='optional')

    if sociallogin.account.provider == 'google':
        username = sociallogin.account.extra_data['name']
        if not user.objects.filter(email=email_address).exists() and not user.objects.filter(username=username).exists():
            new_user, created = user.objects.update_or_create(
                email = email_address,
                username = username,
                is_superuser = False,
                is_premium = False,
                defaults = {
                    'first_name': sociallogin.account.extra_data['given_name'],
                    'last_name': sociallogin.account.extra_data['family_name']
                }
            )
            # verified = sociallogin.account.extra_data['verified_email']
        else:
            if user.objects.filter(email=email_address).exists():
                curr_user = user.objects.filter(email=email_address)
                perform_login(request, curr_user[0], email_verification='optional')

    request.session['project'] = request.session.get('project', None)
    request.session['sub_index'] = request.session.get('sub_index', 0)
    request.session['curr_subdomain'] = request.session.get('curr_subdomain', None)
    request.session.modified = True

    if created:
        new_user.save()
        if new_user:
            perform_login(request, new_user, email_verification='optional')
            raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.user_id)))
    else:
        raise ImmediateHttpResponse(
            redirect('login')
        )