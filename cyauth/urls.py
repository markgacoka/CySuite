from django.urls import path
from . import views

from cyauth.views import (
    registration_view,
    login_view,
    logout_view,
    account_view
)

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registration_view, name="register"),
    path('reset-password/', views.reset_password, name="reset_password"),
    path('account/', account_view, name="account"),
]