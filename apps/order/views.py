from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=user)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'status': 'order cancelled'})
        return Response({'error': 'cannot cancel this order'}, status=400)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__customer__user=user)

@login_required
def order_list(request):
    """Display list of orders for current customer"""
    orders = Order.objects.filter(
        customer=request.user.customer
    ).prefetch_related(
        'items__book',
        'items__shoes',
        'items__clothes',
        'items__mobile'
    ).order_by('-order_date')
    
    return render(request, 'order/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    # Fetch order with all related items
    order = get_object_or_404(
        Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related(
                    'book', 'shoes', 'clothes', 'mobile'
                )
            )
        ),
        id=order_id,
        customer=request.user.customer
    )
    
    # Debug information
    print("\nDebug Order Items:")
    for item in order.items.all():
        print(f"\nItem {item.id}:")
        print(f"Book: {bool(item.book)} (ID: {item.book_id if item.book else None})")
        print(f"Shoes: {bool(item.shoes)} (ID: {item.shoes_id if item.shoes else None})")
        print(f"Clothes: {bool(item.clothes)} (ID: {item.clothes_id if item.clothes else None})")
        print(f"Mobile: {bool(item.mobile)} (ID: {item.mobile_id if item.mobile else None})")
        print(f"Type detected: {item.get_type()}")
    
    return render(request, 'order/order_detail.html', {'order': order})