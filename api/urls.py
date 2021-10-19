from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from .views import ListUrlView, UsersView #UsersView, CurrentUserView

urlpatterns = [
    path('', ListUrlView.as_view(), name='home'),
    
    path('users/', UsersView.as_view(), name='users'),
    # path('current_user/', CurrentUserView.as_view(), name="currentuser"),
    # path('user/<id>', UserView.asView(), name="user"),
    
    path('token/', obtain_auth_token, name='obtain'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]