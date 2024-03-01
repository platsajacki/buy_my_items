from dataclasses import dataclass
from os import getenv

from django.db import transaction
from django.db.models import F, QuerySet, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from stripe import PaymentIntent

from core.services import BaseService
from items.models import Item
from orders.models import Discount, Order

APIS = {
    'usd': getenv('USD_API'),
    'eur': getenv('EUR_API'),
}


@dataclass
class PaymentIntentCreatorService(BaseService):
    request: HttpRequest

    def get_items_queryset(self, item_ids: list[str]) -> QuerySet:
        return (
            Item.objects
            .select_related('tax')
            .filter(
                id__in=list(map(int, item_ids))
            )
            .annotate(total_price=Sum('price'))
        )

    def get_payment_intent(self, order: Order, items: QuerySet) -> PaymentIntent:
        return PaymentIntent.create(
            api_key=APIS[items[0].currency],
            amount=int(items[0].total_price * 100),
            currency=items[0].currency,
            automatic_payment_methods={"enabled": True},
            description=f"Payment for order {order.id}",
        )

    def get_order(self, items: QuerySet) -> Order:
        order = Order.objects.create()
        order.items.add(*items)
        if discount_id := self.request.POST.get('discount_id'):
            discount, _ = Discount.objects.get_or_create(id=discount_id)
            order.discount = discount
        return order

    @transaction.atomic
    def act(self) -> HttpResponseBadRequest | HttpResponse:
        item_ids = self.request.POST.getlist('items')
        if not item_ids:
            return HttpResponseBadRequest()
        items = self.get_items_queryset(item_ids)
        if (count_currency := items.filter(currency=F('currency')).count()) > 1:
            return HttpResponseBadRequest(
                'Order can only contain items with the same currency.'
            )
        if not count_currency:
            return HttpResponseBadRequest()
        order = self.get_order(items)
        return render(
            self.request,
            'checkout.html',
            context={
                'client': self.get_payment_intent(order, items).client_secret,
                'data':
                    {
                        'percent_off': self.request.POST.get('percent_off'),
                        'items': [
                            {
                                'name': item.name,
                                'price': int(item.price * 100),
                                'currency': item.currency,
                                'tax': item.tax.id,
                            }
                            for item in items
                        ]
                    }
                }
            )
