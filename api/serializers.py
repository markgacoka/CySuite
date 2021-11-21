from cyauth.models import Account
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'first_name', 'last_name', 'username', 'occupation', 'email', 'image', 'date_joined', 'last_login', 'is_admin', 'is_premium', 'hide_email', 'feedback', 'api_token', 'badges']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'first_name', 'last_name', 'username', 'occupation', 'email', 'image', 'date_joined', 'last_login', 'is_admin', 'is_premium', 'hide_email', 'feedback', 'api_token', 'badges']