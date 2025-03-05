from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch


from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.order.models import Order, OrderItem
from apps.book.models import Book
from apps.clothes.models import Clothes
from apps.shoes.models import Shoes
from apps.mobiles.models import Mobile  
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer__user=self.request.user)

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        return Response({'status': 'cart cleared'})

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = self.get_object()
   
        return Response({'status': 'checkout initiated'})

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(customer=self.request.user.customer)
        serializer.save(cart=cart)


@login_required
def clear_cart(request):
   
    try:
        cart = Cart.objects.filter(customer=request.user.customer).last()
        if cart:
            cart.items.all().delete()
            messages.success(request, 'Cart cleared successfully.')
        else:
            messages.info(request, 'Cart is already empty.')
    except Exception as e:
        messages.error(request, f'Error clearing cart: {str(e)}')
    return redirect('cart:view_cart')

@login_required
def add_to_cart(request, item_type, item_id):
  
    try:
        cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
        if item_type == 'book':
            item = get_object_or_404(Book, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, book=item, defaults={'quantity': 1}
            )
        elif item_type == 'shoes':
            item = get_object_or_404(Shoes, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, shoes=item, defaults={'quantity': 1}
            )
        elif item_type == 'clothes':
            item = get_object_or_404(Clothes, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, clothes=item, defaults={'quantity': 1}
            )
        elif item_type == 'mobile':
            item = get_object_or_404(Mobile, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, mobile=item, defaults={'quantity': 1}
            )
        else:
            messages.error(request, 'Invalid item type.')
            return redirect('cart:view_cart')
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
       
    except Exception as e:
        messages.error(request, f'Error adding item to cart: {str(e)}')
    
    return redirect('cart:view_cart')

@login_required
def view_cart(request):
   
    cart = Cart.objects.filter(customer=request.user.customer).last()
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
@transaction.atomic
def checkout(request):
   
    cart = Cart.objects.filter(customer=request.user.customer).last()
    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view_cart')
    
    if request.method == 'POST':
        shipping_method = request.POST.get('shipping_method')
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('address')
        
        if shipping_method and payment_method and shipping_address:
            try:
                with transaction.atomic():
                    order = Order.objects.create(
                        customer=request.user.customer,
                        shipping_method=shipping_method,
                        payment_method=payment_method,
                        shipping_address=shipping_address,
                        total_amount=cart.get_total(),  
                        status='confirmed'
                    )
                   
                    for cart_item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            quantity=cart_item.quantity,
                            price=cart_item.get_cost(),
                            book=cart_item.book if hasattr(cart_item, 'book') else None,
                            shoes=cart_item.shoes if hasattr(cart_item, 'shoes') else None,
                            clothes=cart_item.clothes if hasattr(cart_item, 'clothes') else None,
                            mobile=cart_item.mobile if hasattr(cart_item, 'mobile') else None
                        )
                   
                    cart.delete()
                   
                    return redirect('cart:order_confirmation')
            except Exception as e:
                messages.error(request, f'Error during checkout: {str(e)}')
                return redirect('cart:checkout')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'cart/checkout.html', {'cart': cart})

@login_required
def order_confirmation(request):
  
    latest_order = Order.objects.filter(customer=request.user.customer).order_by('-order_date').first()
    if not latest_order:
        messages.error(request, 'No order found.')
        return redirect('cart:view_cart')
    return render(request, 'cart/order_confirmation.html', {'order': latest_order})

@login_required
def update_quantity(request, item_id):
  
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user.customer)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, item_id):
 
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user.customer)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:view_cart')

@login_required
def order_list(request):
 
    orders = Order.objects.filter(customer=request.user.customer).order_by('-order_date')
    return render(request, 'order/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
  
    order = get_object_or_404(
        Order.objects.prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('book', 'shoes', 'clothes', 'mobile'))
        ),
        id=order_id,
        customer=request.user.customer
    )
    return render(request, 'order/order_detail.html', {'order': order})
