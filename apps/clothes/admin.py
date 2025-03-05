from django.contrib import admin
from .models import Clothes

@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'size', 'color', 'price', 'stock')
    list_filter = ('brand', 'size', 'color')
    search_fields = ('title', 'brand', 'description')
    ordering = ('title', 'price')
    list_editable = ('price', 'stock')
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'brand', 'price', 'stock')
        }),
        ('Details', {
            'fields': ('size', 'color', 'description')
        }),
        ('Image', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created_at',)
        return ()