from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "barcode", "price", "stock"]
    list_filter = ["price", "stock"]
    search_fields = ["name", "barcode"]
    ordering = ["name"]
