import importlib

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, View

from .models import Module, ModuleInstallation


class ModulListView(LoginRequiredMixin, ListView):
    template_name = "module_engine/module_list.html"
    model = Module
    queryset = Module.objects.all()


class InstallModulView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        module = get_object_or_404(Module, id=kwargs.get("pk"))

        if module.is_installed(self.request.user):
            messages.warning(self.request, _("Module is already installed."))
            return HttpResponseRedirect(reverse("module_engine:module_list"))

        try:
            # Import the module's install function if it exists
            module_path = f"htt.{module.app_name}.module_utils"
            module_utils = importlib.import_module(module_path)

            if hasattr(module_utils, "install"):
                module_utils.install()

            # Create installation record
            ModuleInstallation.objects.update_or_create(
                module=module,
                installed_by=request.user,
                defaults={
                    "is_installed": True,
                    "version": module.get_version_latest(),
                }
            )

            # Setup permissions
            manager_group = Group.objects.get(name="product_manager")
            self.request.user.groups.add(manager_group)

            messages.success(request, _("Module installed successfully."))
        except (ImportError, AttributeError) as e:
            messages.error(request, _("Error installing module: {}").format(str(e)))

        return HttpResponseRedirect(reverse("module_engine:module_list"))


class UpgradeModulView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        module = get_object_or_404(Module, id=kwargs.get("pk"))

        if not module.is_installed(self.request.user):
            messages.warning(request, _("Module is not installed."))
            return HttpResponseRedirect(reverse("module_engine:module_list"))

        try:
            # Import the module's upgrade function if it exists
            module_path = f"htt.{module.app_name}.module_utils"
            module_utils = importlib.import_module(module_path)

            if hasattr(module_utils, "upgrade"):
                module_utils.upgrade()

            # Update installation record
            ModuleInstallation.objects.update_or_create(
                module=module,
                installed_by=request.user,
                defaults={
                    "version": module.get_version_latest()
                }
            )

            messages.success(request, _("Module upgraded successfully."))
        except (ImportError, AttributeError) as e:
            messages.error(request, _("Error upgrading module: {}").format(str(e)))

        return HttpResponseRedirect(reverse("module_engine:module_list"))


class UninstallModulView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        module = get_object_or_404(Module, id=kwargs.get("pk"))

        if not module.is_installed:
            messages.warning(request, _("Module is not installed."))
            return HttpResponseRedirect(reverse("module_engine:module_list"))

        try:
            # Import the module's uninstall function if it exists
            module_path = f"htt.{module.app_name}.module_utils"
            module_utils = importlib.import_module(module_path)

            if hasattr(module_utils, "uninstall"):
                module_utils.uninstall()

            # Update installation record
            ModuleInstallation.objects.update_or_create(
                module=module,
                installed_by=request.user,
                defaults={
                    "is_installed": False
                }
            )

            # Setup permissions
            manager_group = Group.objects.get(name="product_manager")
            self.request.user.groups.remove(manager_group)

            messages.success(request, _("Module uninstalled successfully."))
        except (ImportError, AttributeError) as e:
            messages.error(request, _("Error uninstalling module: {}").format(str(e)))

        return HttpResponseRedirect(reverse("module_engine:module_list"))
