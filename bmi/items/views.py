from django.views.generic import DetailView, ListView

from items.filters import ItemFilterSet
from items.models import Item


class ItemList(ListView):
    model = Item
    filterset = ItemFilterSet

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset(self.request.GET, queryset=self.queryset)
        return context


class ItemDetail(DetailView):
    model = Item
