import datetime
import importlib

from django.contrib import messages
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

        if module.is_installed:
            messages.warning(request, _("Module is already installed."))
            return HttpResponseRedirect(reverse("module_engine:module_list"))

        try:
            # Import the module's install function if it exists
            module_path = f"htt.{module.app_name}.module_utils"
            module_utils = importlib.import_module(module_path)

            if hasattr(module_utils, "install"):
                module_utils.install()

            # Update module status
            module.is_installed = True
            module.install_date = datetime.datetime.now()
            module.save()

            # Create installation record
            ModuleInstallation.objects.create(
                module=module,
                installed_by=request.user,
                status=ModuleInstallation.StatusChoices.INSTALLED
            )

            messages.success(request, _("Module installed successfully."))
        except (ImportError, AttributeError) as e:
            messages.error(request, _("Error installing module: {}").format(str(e)))

        return HttpResponseRedirect(reverse("module_engine:module_list"))


class UpgradeModulView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        module = get_object_or_404(Module, id=kwargs.get("pk"))

        if not module.is_installed:
            messages.warning(request, _("Module is not installed."))
            return HttpResponseRedirect(reverse("module_engine:module_list"))

        try:
            # Import the module's upgrade function if it exists
            module_path = f"htt.{module.app_name}.module_utils"
            module_utils = importlib.import_module(module_path)

            if hasattr(module_utils, "upgrade"):
                module_utils.upgrade()

            # Update module status
            module.update_date = datetime.datetime.now()
            module.version = request.POST.get("new_version", module.version)
            module.save()

            # Update installation record
            ModuleInstallation.objects.create(
                module=module,
                installed_by=request.user,
                status=ModuleInstallation.StatusChoices.UPGRADING
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

            # Update module status
            module.is_installed = False
            module.save()

            # Update installation record
            ModuleInstallation.objects.create(
                module=module,
                installed_by=request.user,
                status=ModuleInstallation.StatusChoices.UNINSTALLING
            )

            messages.success(request, _("Module uninstalled successfully."))
        except (ImportError, AttributeError) as e:
            messages.error(request, _("Error uninstalling module: {}").format(str(e)))

        return HttpResponseRedirect(reverse("module_engine:module_list"))
