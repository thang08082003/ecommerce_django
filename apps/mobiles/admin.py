from django.contrib import admin
from .models import Mobile

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'storage', 'ram')
    list_filter = ('brand', 'storage', 'ram')
    search_fields = ('title', 'brand', 'description')
    ordering = ('brand', 'title')
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'brand', 'price', 'image')
        }),
        ('Specifications', {
            'fields': ('screen_size', 'storage', 'ram', 'camera')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        })
    )