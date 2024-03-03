import pytest

from django.test import Client
from django.urls import reverse

from items.models import Item

pytestmark = [pytest.mark.django_db]


def test_item_list_view_get_context_data(client: Client):
    response = client.get(reverse('items:index'))
    assert 'filterset' in response.context


@pytest.mark.usefixtures('items')
def test_item_list_view_with_filtering(client: Client):
    count_usd_items = Item.objects.filter(currency='usd').count()
    response = client.get(reverse('items:index'), QUERY_STRING='currency=usd')
    assert len(response.context['filterset'].qs) == count_usd_items
