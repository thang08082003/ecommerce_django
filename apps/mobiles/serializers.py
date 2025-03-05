from rest_framework import serializers
from .models import Mobile

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = [
            'id', 'title', 'brand', 'price', 
            'description', 'image', 'screen_size', 
            'storage', 'ram', 'camera'
        ]