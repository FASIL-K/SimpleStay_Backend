
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.serializers import UserInfoSerializer
from user.models import CustomUser
from .models import *

from rest_framework import viewsets, status




class OwnerSerializer(ModelSerializer):
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

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'user_type', 'is_active', 'is_admin', 'is_staff', 'is_google', 'is_verify', 'date_joined', 'profile_photo']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']
        
class OwnerPostSerializer(serializers.ModelSerializer):
    owner_detail = OwnerSerializer(source="owner", read_only=True)
        # user_main = UserSerializer(source='user', read_only=True)

    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        images_queryset = obj.propertyimage_set.all()
        images_serializer = PropertyImageSerializer(images_queryset, many=True)
        return images_serializer.data
    
    


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'profile_photo']

    def validate_name(self, value):
        # Add validation logic for name if needed
        return value

    def validate_phone(self, value):
        # Add validation logic for phone if needed
        return value