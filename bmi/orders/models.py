from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from items.models import Item


class Discount(models.Model):
    coupon_stripe_id = models.CharField(
        _('coupon stripe id'), max_length=255, unique=True
    )
    percent_off = models.DecimalField(
        _('percent_off'),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        editable=False,
    )

    class Meta:
        ordering = ('percent_off',)
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self) -> str:
        return f'Discount: {self.percent_off}%'


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name=_('items'), related_name='orders')
    discounts = models.ForeignKey(
       'Discount',
       on_delete=models.SET_NULL,
       verbose_name=_('discounts'),
       related_name='orders',
       null=True,
    )

    @property
    def total_discount(self) -> Decimal | int:
        if self.discounts:
            sum_percent_off = sum([d.percent_off for d in self.discounts])
            return sum_percent_off if sum_percent_off < 100 else 100
        return 0

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def clean(self) -> None:
        if len(set(self.items.values_list('currency', flat=True))) > 1:
            raise ValidationError('Order can only contain items with the same currency.')
        super().clean()

    def __str__(self) -> str:
        return f'Order {self.pk}'
