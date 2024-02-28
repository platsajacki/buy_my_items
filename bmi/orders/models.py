from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampedModel, TimestampedModifiedModel
from items.models import Item


class Discount(TimestampedModifiedModel):
    id = models.CharField(_('coupon id'), max_length=255, primary_key=True)

    class Meta:
        ordering = ('modified',)
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self) -> str:
        return f'Coupon: {self.id}'


class Order(TimestampedModel):
    items = models.ManyToManyField(
        Item, verbose_name=_('items'), related_name='orders'
    )
    discounts = models.ForeignKey(
       Discount,
       on_delete=models.SET_NULL,
       verbose_name=_('discounts'),
       related_name='orders',
       null=True,
    )

    class Meta:
        ordering = ('created',)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def clean(self) -> None:
        if len(set(self.items.values_list('currency', flat=True))) > 1:
            raise ValidationError('Order can only contain items with the same currency.')
        super().clean()

    def __str__(self) -> str:
        return f'Order {self.pk}'
