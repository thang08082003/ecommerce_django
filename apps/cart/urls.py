from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/carts', views.CartViewSet, basename='cart-api')
router.register(r'api/cart-items', views.CartItemViewSet, basename='cartitem-api')

app_name = 'cart'

urlpatterns = [
    path('view/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('', include(router.urls)),
]