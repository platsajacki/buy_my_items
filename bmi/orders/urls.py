from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from orders.views import DiscountCheckView, PaymentIntentView, PaymentIntentWebhookView, SucceedOrderTemplateView

app_name = 'purchases'

urlpatterns = [
    path('', PaymentIntentView.as_view(), name='buy'),
    path('webhook/', csrf_exempt(PaymentIntentWebhookView.as_view()), name='webhook'),
    path('succeed-order', SucceedOrderTemplateView.as_view(), name='succeed-order'),
    path('coupons/<str:discount_id>/', DiscountCheckView.as_view(), name='discount-check'),
]
