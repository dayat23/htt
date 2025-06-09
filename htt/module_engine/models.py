from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from htt.users.models import User


class Module(TimeStampedModel):
    """
    Model to store information about available modules.
    """
    name = models.CharField(_("Module Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    app_name = models.CharField(_("App Name"), max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_version_latest()})"

    def is_installed(self, user):
        module_installation = self.moduleinstallation_set.filter(installed_by=user).first()
        return True if module_installation and module_installation.is_installed else False

    def is_upgrading(self, user):
        module_installation = self.moduleinstallation_set.filter(installed_by=user).first()
        version = self.get_version_latest()
        return True if module_installation and module_installation.is_installed and version != module_installation.version else False

    def get_version_latest(self):
        module_version = self.moduleversion_set.order_by("-id").first()
        return module_version.version if module_version else "1"


class ModuleVersion(TimeStampedModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    version = models.CharField(_("Version"), max_length=20)
    description = models.TextField(_("Description"), blank=True)


class ModuleInstallation(TimeStampedModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    installed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_installed = models.BooleanField(_("Is Installed"), default=False)
    installed_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(_("Version"), null=True, max_length=20)
