from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .models import OwnerDetail
from .models import UserDetail

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name','last_name', 'password', 'profile_image', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['user_type'] = user.user_type
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_superuser
        token['is_google'] = user.is_google

        return token

class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email',  'password','first_name','last_name', 'profile_image', 'user_type', 'is_google']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'user_type', 'is_active']

class OwnerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'user_type', 'is_active']


class OwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerDetail
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'