from django.contrib import admin

from .models import Module, ModuleVersion, ModuleInstallation


class ModuleVersionInline(admin.TabularInline):
    model = ModuleVersion
    extra = 0
    min_num = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [ModuleVersionInline]
    list_display = ["name", "app_name"]
    search_fields = ["name", "app_name", "description"]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'app_name', 'description'),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(ModuleInstallation)
class ModuleInstallationAdmin(admin.ModelAdmin):
    raw_id_fields = ["module", "installed_by"]
    list_display = ["module", "version", "is_installed", "installed_by", "installed_at", "modified"]
