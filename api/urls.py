from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ListUrlView, UsersView, UserView, ProjectView, AuthenticatedUser, AuthenticatedProject
from .views import SubdomainView

urlpatterns = [
    path('', ListUrlView.as_view(), name='home'),
    path('token/', obtain_auth_token, name='token'),
    
    # Preserve order of urls - functions like if conditional statements
    # user/ is checked after user/<anything> fails
    # user/<user_id> comes after user/projects as projects can be mistaken for a user_id
    path('users/', UsersView.as_view(), name='users'),  
    path('user/projects/', AuthenticatedProject.as_view(), name="current_project"),
    path('user/<user_id>/', UserView.as_view(), name='modify_user'),
    path('user/<user_id>/projects/', ProjectView.as_view(), name='modify_user_project'),
    path('user/', AuthenticatedUser.as_view(), name="current_user"),

    path('subdomains/<in_scope_domain>/', SubdomainView.as_view(), name="subdomain"),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]