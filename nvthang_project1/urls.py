from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.customer import views as customer_views

urlpatterns = [
  
    path('admin/', admin.site.urls),
    
 
    path('', lambda request: redirect('book:book_list'), name='home'),
    
    path('profile/', customer_views.profile_view, name='profile'), 
    path('customer/', include('apps.customer.urls')),
    path('books/', include('apps.book.urls')),
    path('cart/', include('apps.cart.urls')),
    path('order/', include('apps.order.urls')),
    path('shoes/', include('apps.shoes.urls')),  
    path('clothes/', include('apps.clothes.urls')),  
    path('mobiles/', include('apps.mobiles.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
LOGIN_URL = 'customer:login'
LOGIN_REDIRECT_URL = 'book:book_list'
LOGOUT_REDIRECT_URL = 'customer:login'
"""