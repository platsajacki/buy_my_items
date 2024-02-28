from django_filters import FilterSet
from items.models import Item


class ItemFilterSet(FilterSet):
    class Meta:
        model = Item
        fields = ['currency']
