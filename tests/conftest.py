import pytest
from pytest_mock import MockerFixture

from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from items.models import Item, Tax


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
            name=f'Item {i}',
            description='Item',
            created=dt,
            modified=dt,
            price=Decimal('100.22'),
            currency='usd' if i // 2 == 0 else 'eur',
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
