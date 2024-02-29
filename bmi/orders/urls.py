from django.urls import path

from orders.views import CheckoutTemplateView, DiscountCheckView, PaymentIntentView

app_name = 'purchases'

urlpatterns = [
    path('', PaymentIntentView.as_view(), name='buy'),
    path('', CheckoutTemplateView.as_view(), name='pay'),
    path('coupons/<str:discount_id>/', DiscountCheckView.as_view(), name='discount-check'),
]
