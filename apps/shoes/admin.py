from django.contrib import admin
from .models import Shoes

@admin.register(Shoes)  
class ShoesAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'price', 'size', 'color']
    search_fields = ['title', 'brand']
    list_filter = ['brand', 'size']