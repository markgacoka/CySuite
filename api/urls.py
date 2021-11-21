from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ListUrlView, UsersView, CurrentUserView

urlpatterns = [
    path('', ListUrlView.as_view(), name='home'),
    path('token/', obtain_auth_token, name='token'),
    
    path('users/', UsersView.as_view(), name='users'),
    path('user/', CurrentUserView.as_view(), name="currentuser"),
    # path('user/<id>', UserView.asView(), name="user"),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]