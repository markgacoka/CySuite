from cyauth.models import Account
from main.models import ProjectModel
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'first_name', 'last_name', 'username', 'occupation', 'email', 'image', 'date_joined', 'last_login', 'is_admin', 'is_premium', 'hide_email', 'feedback', 'api_token', 'badges']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'first_name', 'last_name', 'username', 'occupation', 'email', 'image', 'date_joined', 'last_login', 'is_admin', 'is_premium', 'hide_email', 'feedback', 'api_token', 'badges']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ['project_user_id', 'project_name', 'program', 'in_scope_domains', 'progress', 'subdomains']