from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .serializers import BookSerializer
from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.cart.models import Cart, CartItem



@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, book=book)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Increased quantity of {book.title} in your cart')
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            cart=cart,
            book=book,
            quantity=1
        )
        messages.success(request, f'Added {book.title} to your cart')
    
    return redirect('cart:view_cart')

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author']
    ordering_fields = ['price', 'created_at']

    @action(detail=False, methods=['get'])
    def by_author(self, request):
        author = request.query_params.get('author', None)
        books = Book.objects.filter(author=author) if author else []
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        books = Book.objects.filter(stock__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book/book_detail.html', {'book': book})

def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        books = Book.objects.none()
    
    return render(request, 'book/search_results.html', {
        'books': books,
        'query': query
    })
