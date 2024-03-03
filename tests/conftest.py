import pytest

from datetime import datetime
from decimal import Decimal

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
