from django.contrib import admin

from .models import Module, ModuleInstallation


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["name", "app_name", "version", "is_installed", "install_date", "update_date"]
    list_filter = ["is_installed"]
    search_fields = ["name", "app_name", "description"]
    readonly_fields = ["install_date", "update_date"]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'version', 'app_name', 'description'),
        }),
        ('Status', {
            'fields': ('is_installed',),
        }),
    )


@admin.register(ModuleInstallation)
class ModuleInstallationAdmin(admin.ModelAdmin):
    list_display = ["module", "installed_by", "installed_at", "status"]
