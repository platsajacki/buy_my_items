from django.http import HttpRequest, JsonResponse
from django.views import View

from orders.services import DiscountCheckService, PaymentIntentCreatorService


class DiscountCheckView(View):
    def get(self, request: HttpRequest, discount_id: str) -> JsonResponse:
        return DiscountCheckService(request, discount_id)()


class PaymentIntentView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        return PaymentIntentCreatorService(request)()
