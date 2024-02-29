from django.urls import path

from orders.views import DiscountCheckView, PaymentIntentView

app_name = 'purchases'

urlpatterns = [
    path('', PaymentIntentView.as_view(), name='buy'),
    path('coupons/<str:discount_id>/', DiscountCheckView.as_view(), name='discount-check'),
]
