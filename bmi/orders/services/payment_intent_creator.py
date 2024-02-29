from dataclasses import dataclass
from os import getenv

from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
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

    def get_payment_intent(self, order: Order, items: QuerySet) -> PaymentIntent:
        return PaymentIntent.create(
            api_key=APIS[items[0].currency],
            amount=int(sum(items.values_list('price', flat=True)) * 100),
            currency=items[0].currency,
            automatic_payment_methods={"enabled": True},
            description=f"Payment for order {order.id}",
        )

    def get_order(self, items: QuerySet) -> Order:
        order = Order.objects.create()
        order.items.set(items)
        if discount_id := self.request.POST.get('discount_id'):
            discount, _ = Discount.objects.get_or_create(id=discount_id)
            order.discount = discount
        return order

    @transaction.atomic
    def act(self) -> HttpResponseBadRequest | HttpResponseRedirect:
        item_ids = self.request.POST.getlist('items')
        if not item_ids:
            return HttpResponseBadRequest()
        items = Item.objects.filter(
            id__in=list(map(int, item_ids))
        )
        if len(set(items.values_list('currency', flat=True))) > 1:
            return HttpResponseBadRequest(
                'Order can only contain items with the same currency.'
            )
        if not items.exists():
            return HttpResponseBadRequest()
        order = self.get_order(items)
        return render(
            self.request,
            'checkout.html',
            context={'data': self.get_payment_intent(order, items).client_secret}
        )
