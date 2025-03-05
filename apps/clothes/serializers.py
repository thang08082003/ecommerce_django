from rest_framework import serializers
from .models import Clothes

class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = [
            'id', 'title', 'brand', 'description', 'size', 
            'color', 'price', 'stock', 'image', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']