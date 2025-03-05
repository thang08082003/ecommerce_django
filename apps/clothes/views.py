from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Clothes
from .serializers import ClothesSerializer
from apps.cart.models import Cart, CartItem

# ...rest of your existing code...

class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'brand', 'color']
    ordering_fields = ['price', 'created_at']

    @action(detail=False, methods=['get'])
    def by_brand(self, request):
        brand = request.query_params.get('brand', None)
        clothes = Clothes.objects.filter(brand=brand) if brand else []
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_size(self, request):
        size = request.query_params.get('size', None)
        clothes = Clothes.objects.filter(size=size) if size else []
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

def clothes_list(request):
    query = request.GET.get('q')
    if query:
        clothes = Clothes.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        clothes = Clothes.objects.all()
    return render(request, 'clothes/clothes_list.html', {'clothes': clothes, 'query': query})

def clothes_detail(request, clothes_id):
    clothes = get_object_or_404(Clothes, id=clothes_id)
    return render(request, 'clothes/clothes_detail.html', {'clothes': clothes})

@login_required
def add_to_cart(request, clothes_id):
    clothes = get_object_or_404(Clothes, id=clothes_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        clothes=clothes,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart:view_cart')
