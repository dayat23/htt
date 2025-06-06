from django.db import models
from django.utils.translation import gettext_lazy as _


class Module(models.Model):
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
