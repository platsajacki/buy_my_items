from dataclasses import dataclass

from django.http import HttpRequest, HttpResponseNotFound
# from stripe import PaymentIntent

from core.services import BaseService


@dataclass
class OrderCreatorService(BaseService):
    request: HttpRequest

    def act(self) -> HttpResponseNotFound:
        if self.request.POST.getlist('items'):
            return HttpResponseNotFound()
        return HttpResponseNotFound()
