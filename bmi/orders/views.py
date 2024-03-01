from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

from orders.services import DiscountCheckService, PaymentIntentCreatorService


class DiscountCheckView(View):
    def get(self, request: HttpRequest, discount_id: str) -> JsonResponse:
        return DiscountCheckService(request, discount_id)()


class PaymentIntentView(View):
    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseBadRequest:
        return PaymentIntentCreatorService(request)()


class StripeSessionCreateView(View):
    def get(self, request: HttpRequest):
        return
