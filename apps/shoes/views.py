from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Shoes
from .serializers import ShoesSerializer
from apps.cart.models import Cart, CartItem

# ...rest of your existing code...


class ShoesViewSet(viewsets.ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Shoes.objects.all()
        brand = self.request.query_params.get('brand', None)
        size = self.request.query_params.get('size', None)
        
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        if size:
            queryset = queryset.filter(size=size)
            
        return queryset

def shoes_list(request):
    query = request.GET.get('q')
    if query:
        shoes = Shoes.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        shoes = Shoes.objects.all()
    
    paginator = Paginator(shoes, 12)  
    page = request.GET.get('page')
    shoes = paginator.get_page(page)
    
    return render(request, 'shoes/shoes_list.html', {
        'shoes': shoes,
        'query': query
    })

def shoes_detail(request, shoes_id):
    shoes = get_object_or_404(Shoes, id=shoes_id)
    return render(request, 'shoes/shoes_detail.html', {'shoes': shoes})

@login_required
def add_to_cart(request, shoes_id):
    shoes = get_object_or_404(Shoes, id=shoes_id)
    cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        shoes=shoes,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{shoes.title} added to cart.')
    return redirect('cart:view_cart')

def search_shoes(request):
    query = request.GET.get('q', '')
    if query:
        shoes = Shoes.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        shoes = Shoes.objects.none()
    
    return render(request, 'shoes/search_results.html', {
        'shoes': shoes,
        'query': query
    })