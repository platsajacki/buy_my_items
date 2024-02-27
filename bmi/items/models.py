from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampedModel, TimestampedModifiedModel


class Currency(models.TextChoices):
    USD = 'usd', _('dollar')
    EUR = 'eur', _('euro')


class Tax(TimestampedModifiedModel):
    tax_stripe_id = models.CharField(_('tax stripe id'), max_length=255, unique=True)

    class Meta:
        ordering = ('modified',)
        verbose_name = _('tax')
        verbose_name_plural = _('taxes')

    def __str__(self) -> str:
        return f'Tax: {self.rate}'


class Item(TimestampedModel):
    name = models.CharField(
        _('name'), max_length=128
    )
    description = models.TextField(
        _('description'), max_length=512
    )
    price = models.DecimalField(
        _('price'), max_digits=11, decimal_places=2
    )
    currency = models.CharField(
        _('currency'), choices=Currency
    )
    taxes = models.ForeignKey(
        'Tax',
        verbose_name=_('taxes'),
        on_delete=models.SET_NULL,
        related_name='items',
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __str__(self) -> str:
        return self.name
