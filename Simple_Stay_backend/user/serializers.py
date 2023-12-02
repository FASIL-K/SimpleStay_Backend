from .models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserGoogleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name','email','user_type','is_active','is_google']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

        


class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        
        if not user.is_active:
            raise ValidationError('User is not active', code='inactive_user')
        

        print(user.email) # type: ignore
        token['id'] = user.id # type: ignore
        token['email'] = user.email  # type: ignore
        token['user_type'] = user.user_type # type: ignore
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_admin 
        token['is_google'] = user.is_google

        
        return token
