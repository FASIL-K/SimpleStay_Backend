
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

class OwnerinfoSerializer(serializers.ModelSerializer):
    class meta:
        model = OwnerInfo
        fields = "__all__"


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class OwnerPostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        images_queryset = obj.propertyimage_set.all()
        images_serializer = PropertyImageSerializer(images_queryset, many=True)
        return images_serializer.data

