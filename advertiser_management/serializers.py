from rest_framework import serializers
from advertiser_management.models import Ad, Advertiser
class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class AdvertiserSerializer(serializers.ModelSerializer):
    ads =AdSerializer(many=True, read_only=True)
    class Meta:
        model = Advertiser
        fields = ['id', 'name', 'ads']

class AdGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'image']