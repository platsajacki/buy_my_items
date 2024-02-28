from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView

from orders.services import OrderCreatorService


class OrderCreateView(CreateView):
    http_method_names = ['post']

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return OrderCreatorService(request)()
