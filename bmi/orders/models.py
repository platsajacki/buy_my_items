from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampedModel, TimestampedModifiedModel
from items.models import Item


class Discount(TimestampedModifiedModel):
    coupon_stripe_id = models.CharField(_('coupon stripe id'), max_length=255, unique=True)

    class Meta:
        ordering = ('modified',)
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self) -> str:
        return f'Discount: {self.percent_off}%'


class Order(TimestampedModel):
    items = models.ManyToManyField(
        Item, verbose_name=_('items'), related_name='orders'
    )
    discounts = models.ManyToManyField(
       Discount, verbose_name=_('discounts'), related_name='orders',
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
