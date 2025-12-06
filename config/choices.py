from django.utils.translation import ugettext_lazy as _
from django.db import models


class RoleChoices(models.TextChoices):
    SHOP_ADMIN = 'shop_admin', _("Shop Admin")
    BRANCH_ADMIN = 'branch_admin', _("Branch Admin")
    CASHIER = 'cashier', _('Cashier')


class CurrencyChoices(models.TextChoices):
    RUBLE = 'ruble', _("Ruble")
    DOLLAR = 'dollar', _("Dollar")
    COM = 'com', _('Com')


class MeasurementChoices(models.TextChoices):
    PIECE = 'piece', 'Штук'
    KILOGRAM = 'kilogram', 'Килограмм'
