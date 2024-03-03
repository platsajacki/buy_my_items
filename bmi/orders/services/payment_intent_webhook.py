from dataclasses import dataclass

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from stripe import Webhook, error

from core.services import BaseService
from orders.models import Order


@dataclass
class PaymentIntentWebhookService(BaseService):
    request:  HttpRequest

    def act(self) -> JsonResponse:
        try:
            event = Webhook.construct_event(
                self.request.body,
                self.request.headers['STRIPE_SIGNATURE'],
                settings.WH_PAYMENT_INTENT,
            )
            order_id = event['data']['object']['metadata']['order']
        except ValueError as e:
            raise e
        except error.SignatureVerificationError as e:  # type: ignore[attr-defined]
            raise e
        order = get_object_or_404(Order, id=order_id)
        match event['type']:
            case 'payment_intent.canceled':
                order.status = 'canceled'
            case 'payment_intent.succeeded':
                order.status = 'succeeded'
            case 'payment_intent.payment_failed':
                order.status = 'failed'
        order.save()
        return JsonResponse({'success': True})
