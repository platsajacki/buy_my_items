from django.views.generic import ListView

from items.models import Item


class ItemList(ListView):
    model = Item
