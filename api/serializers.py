from cyauth.models import Account
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'is_premium', 'hide_email', 'feedback']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'is_premium', 'hide_email', 'feedback']