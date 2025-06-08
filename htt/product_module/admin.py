from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ["created_by"]
    list_display = ["name", "barcode", "price", "stock", "created_by"]
    list_filter = ["price", "stock"]
    search_fields = ["name", "barcode"]
    ordering = ["name"]
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'barcode', 'price', 'stock'),
        }),
        ('Metadata', {
            'fields': ('created_by',),
        }),
    )
