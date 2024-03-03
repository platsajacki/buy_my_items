import pytest
from pytest_mock import MockerFixture

import json
from http import HTTPStatus
from unittest.mock import Mock

from django.conf import settings
from django.test import Client
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_discount_check_with_valid_response(client: Client, mocker: MockerFixture, coupon_return_value: Mock):
    mock = mocker.patch('stripe.Coupon.retrieve', return_value=coupon_return_value)
    response = client.get(reverse('purchases:discount-check', kwargs={'discount_id': coupon_return_value.id}))

    mock.assert_called_once_with(id=coupon_return_value.id, api_key=settings.USD_API)
    assert response.status_code == HTTPStatus.OK
    expected_json = {
        'id': coupon_return_value.id,
        'percent_off': coupon_return_value.percent_off
    }
    assert json.loads(response.content) == expected_json


def test_discount_check_with_invalid_coupon(client: Client, mocker: MockerFixture, coupon_return_value: Mock):
    coupon_return_value.valid = False
    mock = mocker.patch('stripe.Coupon.retrieve', return_value=coupon_return_value)
    response = client.get(reverse('purchases:discount-check', kwargs={'discount_id': coupon_return_value.id}))

    mock.assert_called_once_with(id=coupon_return_value.id, api_key=settings.USD_API)
    assert response.status_code == HTTPStatus.BAD_REQUEST
