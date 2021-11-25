from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ListUrlView, UsersView, UserView, ProjectView, AuthenticatedUser

urlpatterns = [
    path('', ListUrlView.as_view(), name='home'),
    path('token/', obtain_auth_token, name='token'),
    
    path('users/', UsersView.as_view(), name='users'),
    path('user/', AuthenticatedUser.as_view(), name="currentuser"),
    path('user/<user_id>/', UserView.as_view(), name='modify_user'),
    path('user/projects/', ProjectView.as_view(), name="project"),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]