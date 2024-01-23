from rest_framework import serializers
from .models import SavedPost
from owner.serializers import OwnerPostSerializer


class SavedCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=SavedPost
        fields='__all__'


class SavedListSerializer(serializers.ModelSerializer):
    post=OwnerPostSerializer(read_only=True)
    class Meta:
        model=SavedPost
        fields='__all__'
