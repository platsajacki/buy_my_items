import pytest
from pytest_mock import MockerFixture

from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from items.models import Item, Tax
from orders.models import Discount, Order


@pytest.fixture
def tax() -> Tax:
    return Tax.objects.create(
        id='txcd_00000000',
        type='physical',
        name='tax',
        description='tax',
        modified=datetime.now(),
    )


@pytest.fixture
def item(tax: Tax) -> Item:
    dt = datetime.now()
    return Item.objects.create(
        name='Item',
        description='Item',
        created=dt,
        modified=dt,
        price=Decimal('100.22'),
        currency='usd',
        tax=tax,
    )


@pytest.fixture
def items(tax: Tax) -> list[Item]:
    dt = datetime.now()
    instances = [
        Item(
            id=i + 1,
            name=f'Item {i}',
            description='Item',
            created=dt,
            modified=dt,
            price=Decimal('100.22'),
            currency='usd' if i == 0 else 'eur',
            tax=tax,
        ) for i in range(5)
    ]
    return Item.objects.bulk_create(instances)


@pytest.fixture
def coupon_return_value(mocker: MockerFixture) -> Mock:
    mock = mocker.Mock()
    mock.id = 'first'
    mock.percent_off = 10
    mock.valid = True
    return mock


@pytest.fixture
def discount() -> Discount:
    return Discount.objects.create(id='first')


@pytest.fixture
def order(items: list[Item], discount: Discount) -> Order:
    order = Order.objects.create(discount=discount)
    order.items.add(*items)
    return order


@pytest.fixture(
    params=[
        ('payment_intent.canceled', 'canceled'),
        ('payment_intent.payment_failed', 'failed'),
        ('payment_intent.succeeded', 'succeeded'),
    ]
)
def event_data(request, order: Order) -> dict:
    return {
        'type': request.param[0],
        'data': {
            'object': {
                'metadata': {'order': order.id}
            }
        },
        'expected_status': request.param[1]
    }


@pytest.fixture
def payment_intent_return_value(mocker: MockerFixture) -> Mock:
    mock = mocker.Mock()
    mock.client_secret = 'mocked_client_secret'
    mock.amount = 2000
    return mock


@pytest.fixture
def calculation_return_value(mocker: MockerFixture) -> Mock:
    mock = mocker.Mock()
    mock.api_key = 'mocked_api_key'
    mock.currency = 'usd'
    mock.amount_total = 2000
    mock.tax_amount_exclusive = 100
    return mock


@pytest.fixture
def mock_payment_service_methods(
    mocker: MockerFixture, calculation_return_value: Mock, payment_intent_return_value: Mock
) -> None:
    mocker.patch(
        'orders.services.PaymentIntentCreatorService.calculate_tax', return_value=calculation_return_value
    )
    mocker.patch(
        'orders.services.PaymentIntentCreatorService.get_payment_intent', return_value=payment_intent_return_value
    )
