from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from stripe import Coupon, InvalidRequestError

from core.services import BaseService


@dataclass
class DiscountCheckService(BaseService):
    request: HttpRequest
    discount_id: str

    def act(self) -> Any:
        try:
            coupon = Coupon.retrieve(id=self.discount_id, api_key=settings.USD_API)
            if not coupon.valid:
                return JsonResponse({'error': 'Coupon is not active.'}, status=400)
        except InvalidRequestError:
            return JsonResponse({'error': 'Coupon not found.'}, status=400)
        return JsonResponse(
            {
                'id': coupon.id,
                'percent_off': coupon.percent_off
            }
        )
