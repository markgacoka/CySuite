from .views import TestView
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', TestView.as_view(), name='home'),
    path('token/', obtain_auth_token, name='obtain'),
    path('api-auth/', include('rest_framework.urls')),
]