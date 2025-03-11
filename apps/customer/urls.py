from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'api/customers', views.CustomerViewSet, basename='customer-api')
app_name = 'customer'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
   
    path('login/', auth_views.LoginView.as_view(template_name='customer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='customer:login'), name='logout'),
    path('', include(router.urls)),
    
    
]
