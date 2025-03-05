from rest_framework import serializers
from .models import Order, OrderItem
from apps.customer.serializers import CustomerSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    shoes_title = serializers.CharField(source='shoes.title', read_only=True)
    clothes_title = serializers.CharField(source='clothes.title', read_only=True)
    mobile_title = serializers.CharField(source='mobile.title', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'book', 'shoes', 'clothes', 'mobile',
            'book_title', 'shoes_title', 'clothes_title', 'mobile_title',
            'quantity', 'price', 'get_total'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_items = serializers.IntegerField(source='get_total_items', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_details', 'order_date', 
            'status', 'status_display', 'shipping_method', 
            'payment_method', 'shipping_address', 'total_amount',
            'total_items', 'items'
        ]