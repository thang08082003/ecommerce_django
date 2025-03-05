from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(source='get_type', read_only=True)
    title = serializers.CharField(source='get_title', read_only=True)
    cost = serializers.DecimalField(source='get_cost', max_digits=10, decimal_places=2, read_only=True)
    image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'book', 'shoes', 'clothes', 'mobile',
            'quantity', 'item_type', 'title', 'cost', 'image_url'
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(source='get_total', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']