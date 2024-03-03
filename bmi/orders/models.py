from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampedCreatedModel, TimestampedModel
from items.models import Item


class Status(models.TextChoices):
    CREATED = 'created', _('created')
    CANCELED = 'canceled', _('canceled')
    FAILED = 'failed', _('failed')
    SUCCEEDED = 'succeeded', _('succeeded')


class Discount(TimestampedCreatedModel):
    id = models.CharField(_('id'), max_length=255, primary_key=True)

    class Meta:
        ordering = ('created',)
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self) -> str:
        return f'Coupon: {self.id}'


class Order(TimestampedModel):
    items = models.ManyToManyField(
        Item, verbose_name=_('items'), related_name='orders'
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, related_name='orders'
    )
    status = models.CharField(
        _('status'), choices=Status, default=Status.CREATED
    )

    class Meta:
        ordering = ('created',)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self) -> str:
        return f'Order {self.pk}'
