from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('account/', account_view, name="account"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/', account_view, name="profile"),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), 
        name='password_change_done'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='auth/password_change.html'), 
        name='password_change'),
    path('password-reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset.html'), name='password_reset_confirm'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='auth/forgot-password.html'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
        name='password_reset_complete'),
]