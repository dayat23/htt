from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Model to store product information.
    """
    name = models.CharField(_("Name"), max_length=100)
    barcode = models.CharField(_("Barcode"), max_length=50, unique=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Stock"), default=0)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["name"]

    def __str__(self):
        return self.name
