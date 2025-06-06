from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["name", "app_name", "version", "is_installed", "install_date", "update_date"]
    list_filter = ["is_installed"]
    search_fields = ["name", "app_name", "description"]
    readonly_fields = ["install_date", "update_date"]
