from dataclasses import dataclass
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from stripe import PaymentIntent
from stripe.tax import Calculation

from core.services import BaseService
from items.models import Item
from orders.models import Discount, Order

APIS = {
    'usd': settings.USD_API,
    'eur': settings.EUR_API,
}

TEST_CUSTOMER_DETAILS = {
    'address': {
        'line1': '920 5th Ave',
        'city': 'Seattle',
        'state': 'WA',
        'postal_code': '98104',
        'country': 'US',
        },
    'address_source': 'shipping',
}
"""So we don't have the customer's data, we use test ones."""


@dataclass
class PaymentIntentCreatorService(BaseService):
    request: HttpRequest

    def get_items_queryset(self, item_ids: list[str]) -> QuerySet:
        return Item.objects.select_related('tax').filter(id__in=list(map(int, item_ids)))

    def calculate_tax(self, items: QuerySet[Item], percent_off: str | None) -> Calculation:
        return Calculation.create(
            api_key=APIS[items[0].currency],
            currency=items[0].currency,
            customer_details=TEST_CUSTOMER_DETAILS,  # type: ignore[arg-type]
            expand=['line_items'],
            line_items=[
                {
                    'reference': f'№{item.id}. {item.name}',
                    'amount': (
                        int(item.price * 100) - int(item.price * Decimal(percent_off))
                        if percent_off else
                        int(item.price * 100)
                    ),
                    'tax_code': item.tax.id,
                }
                for item in items
            ]
        )

    def get_payment_intent(self, order: Order, calculation_taxs: Calculation) -> PaymentIntent:
        return PaymentIntent.create(
            api_key=calculation_taxs.api_key,
            amount=calculation_taxs.amount_total,
            currency=calculation_taxs.currency,
            description=f'Payment for order {order.id}',
        )

    def get_order(self, items: QuerySet) -> Order:
        order = Order.objects.create()
        order.items.add(*items)
        if discount_id := self.request.POST.get('discount_id'):
            discount, _ = Discount.objects.get_or_create(id=discount_id)
            order.discount = discount
            order.save()
        return order

    @transaction.atomic
    def act(self) -> HttpResponseBadRequest | HttpResponse:
        item_ids = self.request.POST.getlist('items')
        if not item_ids:
            return HttpResponseBadRequest()
        items = self.get_items_queryset(item_ids)
        if (count_currency := items.values('currency').distinct().count()) > 1:
            return HttpResponseBadRequest(
                'Order can only contain items with the same currency.'
            )
        if not count_currency:
            return HttpResponseBadRequest()
        percent_off = self.request.POST.get('percent_off')
        order = self.get_order(items)
        calculation_taxs = self.calculate_tax(items, percent_off)
        payment_intent = self.get_payment_intent(order, calculation_taxs)
        return render(
            self.request,
            'checkout.html',
            context={
                'client': payment_intent.client_secret,
                'return_url': reverse('items:index'),
                'total_amount': payment_intent.amount / 100,
                'discount': order.discount,
                'percent_off': percent_off,
                'items': items,
                'tax': calculation_taxs.tax_amount_inclusive / 100,
            }
        )
