from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'api/shoes', views.ShoesViewSet, basename='shoes-api')

app_name = 'shoes'

urlpatterns = [
    # Regular web URLs
    path('', views.shoes_list, name='shoes_list'),
    path('<int:shoes_id>/', views.shoes_detail, name='shoes_detail'),
    path('add/<int:shoes_id>/', views.add_to_cart, name='add_to_cart'),
    path('search/', views.search_shoes, name='search_shoes'),
    
    # API URLs
    path('', include(router.urls)),
]