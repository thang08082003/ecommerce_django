from django.urls import path
from . import views

app_name = 'mobiles'

urlpatterns = [
    path('', views.mobiles_list, name='mobiles_list'),
    path('<int:mobile_id>/', views.mobile_detail, name='mobile_detail'),
    path('search/', views.search_mobiles, name='search_mobiles'),
    path('add-to-cart/<int:mobile_id>/', views.add_to_cart, name='add_to_cart'),
]