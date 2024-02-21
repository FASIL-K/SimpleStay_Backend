from rest_framework import serializers
from .models import PremiumPackages,PremiumOwner
from owner.serializers import OwnerSerializer

class PremiumPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPackages
        fields = '__all__'

class PremiumOwnerSerializer(serializers.ModelSerializer):
    package_details = PremiumPackagesSerializer(source='package', read_only=True)
    user_details = OwnerSerializer(source='user', read_only=True)

    class Meta:
        model = PremiumOwner
        fields = '__all__'