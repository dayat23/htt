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
    version = models.CharField(_("Version"), max_length=20)
    is_installed = models.BooleanField(_("Is Installed"), default=False)
    install_date = models.DateTimeField(_("Install Date"), null=True, blank=True)
    update_date = models.DateTimeField(_("Update Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.version})"


class ModuleInstallation(TimeStampedModel):

    class StatusChoices(models.TextChoices):
        INSTALLING = "installing", "Installing"
        INSTALLED = "installed", "Installed"
        UPGRADING = "upgrading", "Upgrading"
        UNINSTALLING = "uninstalling", "Uninstalling"
        FAILED = "failed", "Failed"

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    installed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    installed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices)
