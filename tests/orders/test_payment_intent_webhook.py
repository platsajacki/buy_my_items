import pytest
from pytest_mock import MockerFixture

from http import HTTPStatus

from django.http import HttpRequest
from django.test import Client
from django.urls import reverse

from orders.models import Order

pytestmark = [pytest.mark.django_db]


def test_webhook(client: Client, event_data: dict, order: Order, mocker: MockerFixture):
    mocker.patch('stripe.Webhook.construct_event', return_value=event_data)
    mocker.patch.object(
        HttpRequest, 'headers', new_callable=mocker.PropertyMock, return_value={'STRIPE_SIGNATURE': 'STRIPE_SIGNATURE'}
    )
    response = client.post(reverse('purchases:webhook'))
    order.refresh_from_db()
    assert order.status == event_data['expected_status']
    assert response.status_code == HTTPStatus.OK
