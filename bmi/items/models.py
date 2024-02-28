from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import NameModel, TimestampedModel, TimestampedModifiedModel


class Currency(models.TextChoices):
    USD = 'usd', _('dollar')
    EUR = 'eur', _('euro')


class TypeItem(models.TextChoices):
    PHYSICAL = 'physical', _('physical')
    SERVICES = 'services', _('services')
    DIGITAL = 'digital', _('digital')


class Tax(NameModel, TimestampedModifiedModel):
    id = models.CharField(
        _('id'), max_length=50, primary_key=True
    )
    type = models.CharField(
        _('type'), max_length=50, choices=TypeItem
    )
    description = models.TextField(
        _('description'), max_length=512
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('tax')
        verbose_name_plural = _('taxes')


class Item(NameModel, TimestampedModel):
    description = models.TextField(
        _('description'), max_length=1024
    )
    price = models.DecimalField(
        _('price'), max_digits=11, decimal_places=2
    )
    currency = models.CharField(
        _('currency'), choices=Currency
    )
    tax = models.ForeignKey(
        'Tax',
        verbose_name=_('taxes'),
        on_delete=models.PROTECT,
        related_name='items',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('item')
        verbose_name_plural = _('items')
