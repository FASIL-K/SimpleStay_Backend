from rest_framework.serializers import ModelSerializer
from .models import Message
from user.models import CustomUser
# from company.models import ApplyJobs
from rest_framework import serializers


class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']

class UserListSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'