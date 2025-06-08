from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from htt.users.models import User


class Product(TimeStampedModel):
    """
    Model to store product information.
    """
    name = models.CharField(_("Name"), max_length=100)
    barcode = models.CharField(_("Barcode"), max_length=50, unique=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Stock"), default=0)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="created_products")

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["name"]
        permissions = [
            ("can_manage_products", "Can manage all products"),
            ("can_edit_products", "Can edit products"),
            ("can_view_products", "Can view products"),
        ]

    def __str__(self):
        return self.name
