from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from rest_framework.authtoken.models import Token
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
        if sociallogin.is_existing:
            return

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    created = False
    user = get_user_model()
    email_address = sociallogin.account.extra_data['email']

    if sociallogin.account.provider == 'github':
        name = sociallogin.account.extra_data['name'].split()
        username = sociallogin.account.extra_data['login']
        image = sociallogin.account.extra_data['avatar_url']
        social_provider = 'Github'
        company = sociallogin.account.extra_data['company']
        if len(name) == 2:
            last_name = name[1]
        elif len(name) > 2:
            last_name = name[-1]
        else:
            last_name = ''

        if user.objects.filter(email=email_address).exists() and user.objects.filter(email=email_address).values_list('social_provider')[0][0] == 'Github':
            curr_user = user.objects.filter(email=email_address)
            perform_login(request, curr_user[0], email_verification='optional')
        elif user.objects.filter(email=email_address).exists() and user.objects.filter(email=email_address).values_list('social_provider')[0][0] != 'Github':
            curr_user = user.objects.filter(email=email_address)
            sociallogin.connect(request, curr_user[0])
            perform_login(request, curr_user[0], email_verification='optional')
        else:
            new_user, created = user.objects.update_or_create(
                username = username,
                email = email_address,
                social_provider = social_provider,
                is_admin = False,
                is_premium = False,
                is_repo_linked = True,
                defaults = {
                    'first_name': name[0],
                    'last_name': last_name,
                    'company': company,
                    'image': image
                }
            )
            # verified = sociallogin.account.extra_data['verified']

    if sociallogin.account.provider == 'gitlab':
        username = sociallogin.account.extra_data['name']
        social_provider = 'Gitlab'
        if user.objects.filter(email=email_address).exists() and user.objects.filter(email=email_address).values_list('social_provider')[0][0] == 'Gitlab':
            curr_user = user.objects.filter(email=email_address)
            perform_login(request, curr_user[0], email_verification='optional')
        elif user.objects.filter(email=email_address).exists() and user.objects.filter(email=email_address).values_list('social_provider')[0][0] != 'Gitlab':
            curr_user = user.objects.filter(email=email_address)
            sociallogin.connect(request, curr_user[0])
            perform_login(request, curr_user[0], email_verification='optional')
        else:
            new_user, created = user.objects.update_or_create(
                email = email_address,
                username = username,
                social_provider = social_provider,
                is_admin = False,
                is_premium = False,
                is_repo_linked = True,
                defaults = {
                    'first_name': sociallogin.account.extra_data['first_name'],
                    'last_name': sociallogin.account.extra_data['last_name']
                }
            )
            # verified = sociallogin.account.extra_data['verified']

    if sociallogin.account.provider == 'google':
        username = sociallogin.account.extra_data['name']
        social_provider = 'Google'
        if user.objects.filter(email=email_address).exists() and user.objects.filter(email=email_address).values_list('social_provider')[0][0] == 'Google':
            curr_user = user.objects.filter(email=email_address)
            perform_login(request, curr_user[0], email_verification='optional')
        elif user.objects.filter(email=email_address).exists() and user.objects.filter(email=email_address).values_list('social_provider')[0][0] != 'Google':
            curr_user = user.objects.filter(email=email_address)
            sociallogin.connect(request, curr_user[0])
            perform_login(request, curr_user[0], email_verification='optional')
        else:
            new_user, created = user.objects.update_or_create(
                email = email_address,
                username = username,
                social_provider = social_provider,
                is_superuser = False,
                is_premium = False,
                is_repo_linked = False,
                defaults = {
                    'first_name': sociallogin.account.extra_data['given_name'],
                    'last_name': sociallogin.account.extra_data['family_name']
                }
            )
            # verified = sociallogin.account.extra_data['verified_email']

    redirect('set-password')
    request.session['project'] = request.session.get('project', None)
    request.session['sub_index'] = request.session.get('sub_index', 0)
    request.session['curr_subdomain'] = request.session.get('curr_subdomain', None)
    request.session.modified = True

    if created:
        new_user.api_token = Token.objects.get(user_id=new_user.user_id).key
        new_user.save()
        if new_user:
            pass
    else:
        raise ImmediateHttpResponse(
            redirect('login')   
        )