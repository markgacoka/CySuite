from django.urls import path, include
from django.conf.urls import url
from . import views
from .views import TestView

urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.home, name='home'),
]