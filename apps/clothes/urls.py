from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'api/clothes', views.ClothesViewSet, basename='clothes-api')
app_name = 'clothes'

urlpatterns = [
    path('', views.clothes_list, name='clothes_list'),
    path('<int:clothes_id>/', views.clothes_detail, name='clothes_detail'),
    path('add-to-cart/<int:clothes_id>/', views.add_to_cart, name='add_to_cart'),
    path('', include(router.urls)),
]