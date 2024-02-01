
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
        fields = ['id', 'name', 'email', 'phone', 'user_type', 'is_active', 'is_admin', 'is_staff', 'is_google', 'is_verify', 'date_joined', 'profile_photo','is_premium']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'  # Add specific fields if needed

class OwnerPostSerializer(serializers.ModelSerializer):
    owner_detail = OwnerSerializer(source="owner", read_only=True)
    amenities = AmenitySerializer(many=True, required=False)  # Allow amenities to be optional during creation
    images = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        images_queryset = obj.propertyimage_set.all()
        images_serializer = PropertyImageSerializer(images_queryset, many=True)
        return images_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Use the related manager to get amenities for the current post
        amenities_queryset = instance.amenitie.all()
        amenities_serializer = AmenitySerializer(amenities_queryset, many=True)

        # Add post and owner details to the response
        representation['amenities'] = amenities_serializer.data
        representation['owner_details'] = OwnerSerializer(instance.owner).data  

        return representation
    def create(self, validated_data):
        amenities_data = self.context['request'].data.get('amenities', '')
        amenities_list = [{"name": amenity} for amenity in amenities_data.split(',')]
        validated_data.pop('amenities', None)
        property_instance = Post.objects.create(**validated_data)

        for amenity_data in amenities_list:
            amenity, created = Amenity.objects.get_or_create(name=amenity_data['name'], post=property_instance)

        return property_instance


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'profile_photo','is_premium']

    def validate_name(self, value):
        # Add validation logic for name if needed
        return value

    def validate_phone(self, value):
        # Add validation logic for phone if needed
        return value