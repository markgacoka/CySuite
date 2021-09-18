from django.urls import path
from django.conf.urls import url
from . import views

from main.views import (
    update_transaction
)

urlpatterns = [
    #main-pages
    url(r'^transaction/', update_transaction, name='transaction'),
    path('checkout/', views.checkout, name='checkout'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    #dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
    path('projects/', views.projects, name='projects'),
    path('stats/', views.stats, name='stats'),
    path('subdomain-enum/', views.subdomain_enum, name='subdomain_enum'),
    path('directory-enum/', views.directory_enum, name='directory_enum'),
    path('vuln-analysis/', views.vuln_analysis, name='vuln_analysis'),
    path('dorking/', views.dorking, name='dorking'),
    path('exploit/', views.exploit, name='exploit'),
    path('req-tamperer/', views.req_tamperer, name='req_tamperer'),
    path('wordlist-gen/', views.wordlist_gen, name='wordlist_gen'),
    path('decoder/', views.decoder, name='decoder'),
    path('injector/', views.injector, name='injector'),
]