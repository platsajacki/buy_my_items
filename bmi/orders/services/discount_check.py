from dataclasses import dataclass
from os import getenv
from typing import Any

from django.http import HttpRequest, JsonResponse
from stripe import Coupon, InvalidRequestError

from core.services import BaseService

USD_API = getenv('USD_API')


@dataclass
class DiscountCheckService(BaseService):
    request: HttpRequest
    discount_id: str

    def act(self) -> Any:
        try:
            coupon = Coupon.retrieve(id=self.discount_id, api_key=USD_API)
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
