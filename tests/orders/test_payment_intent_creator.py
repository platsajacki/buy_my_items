import pytest

from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from orders.models import Discount, Order

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('items', 'mock_payment_service_methods')]


def test_payment_intant_creator_with_full_valid_data(client: Client):
    data = {
        'items': ['2', '4'],
        'discount_id': 'first',
        'percent_off': '10',
    }
    response = client.post(reverse('purchases:buy'), data=data)
    order = Order.objects.first()
    assert order is not None
    assert order.discount == Discount.objects.get(id=data['discount_id'])
    assert list(order.items.values_list('id', flat=True)) == list(map(int, data['items']))
    assert response.status_code == HTTPStatus.OK


def test_payment_intant_creator_with_invalid_items_data(client: Client):
    response = client.post(reverse('purchases:buy'), data={'items': []})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_payment_intant_creator_with_different_currency_items_data(client: Client):
    response = client.post(reverse('purchases:buy'), data={'items': ['1', '2']})
    assert response.status_code == HTTPStatus.BAD_REQUEST
