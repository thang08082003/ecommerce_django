from django.db import router
from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/orders', views.OrderViewSet, basename='order-api')
router.register(r'api/order-items', views.OrderItemViewSet, basename='orderitem-api')
app_name = 'order'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
]