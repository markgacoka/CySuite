from django.urls import path
from . import views

from cyauth.views import (
    registration_view,
    login_view,
    logout_view,
    account_view
)

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registration_view, name="register"),
    path('reset-password/', views.reset_password, name="reset_password"),
    path('account/', account_view, name="account"),
    path('dashboard/', views.dashboard, name="dashboard"),
]