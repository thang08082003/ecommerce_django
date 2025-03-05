from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Mobile
from .serializers import MobileSerializer
from apps.cart.models import Cart, CartItem

# ...rest of your existing code...
class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

def mobiles_list(request):
    query = request.GET.get('q')
    if query:
        mobiles = Mobile.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        mobiles = Mobile.objects.all()
    return render(request, 'mobiles/mobiles_list.html', {'mobiles': mobiles, 'query': query})

def mobile_detail(request, mobile_id):
    mobile = get_object_or_404(Mobile, id=mobile_id)
    return render(request, 'mobiles/mobile_detail.html', {'mobile': mobile})

@login_required
def add_to_cart(request, mobile_id):
    mobile = get_object_or_404(Mobile, id=mobile_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        mobile=mobile,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart:view_cart')

def search_mobiles(request):
    query = request.GET.get('q', '')
    if query:
        mobiles = Mobile.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        mobiles = Mobile.objects.none()
    
    return render(request, 'mobiles/search_results.html', {
        'mobiles': mobiles,
        'query': query
    })
def mobiles_list(request):
    query = request.GET.get('q')
    if query:
        mobiles = Mobile.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        mobiles = Mobile.objects.all()
    return render(request, 'mobiles/mobiles_list.html', {'mobiles': mobiles, 'query': query})