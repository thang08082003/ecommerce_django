from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm
from apps.order.models import Order
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user=user)

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.orders.all()
       
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer:profile')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'customer/register.html', {'form': form})

@login_required
def profile(request):
    # Get all orders for the current user, ordered by most recent first
    orders = Order.objects.filter(
        customer=request.user.customer
    ).order_by('-order_date')
    
    return render(request, 'customer/profile.html', {
        'user': request.user,
        'orders': orders
    })

def profile_view(request):
    return render(request, 'customer/profile.html')