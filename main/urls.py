from django.urls import path
from . import views

urlpatterns = [
    #main-pages
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    #dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.projects, name='projects'),
    path('notes/', views.notes, name='notes'),
    path('subdomain-enum/', views.subdomain_enum, name='subdomain_enum'),
    path('directory-enum/', views.directory_enum, name='directory_enum'),
    path('vuln-analysis/', views.vuln_analysis, name='vuln_analysis'),
    path('dorking/', views.dorking, name='dorking'),
    path('exploit/', views.exploit, name='exploit'),
    path('req-tamperer/', views.req_tamperer, name='req_tamperer'),
    path('wordlist-gen/', views.wordlist_gen, name='wordlist_gen'),
    path('decoder/', views.decoder, name='decoder'),
    path('file-upload/', views.file_upload, name='file_upload'),
    #notes
    path('notes/post-1', views.post, name='post'),
]