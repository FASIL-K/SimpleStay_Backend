
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import CustomUser




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
        fields = ['id','name','email','role','is_active','is_google']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
