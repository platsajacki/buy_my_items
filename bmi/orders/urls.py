from django.urls import path

from orders.views import DiscountCheckView, PaymentIntentView, SucceedOrderTemplateView

app_name = 'purchases'

urlpatterns = [
    path('', PaymentIntentView.as_view(), name='buy'),
    path('succeed-order', SucceedOrderTemplateView.as_view(), name='succeed-order'),
    path('coupons/<str:discount_id>/', DiscountCheckView.as_view(), name='discount-check'),
]
