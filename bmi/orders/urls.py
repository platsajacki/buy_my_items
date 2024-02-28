from django.urls import path

from orders.views import OrderCreateView

app_name = 'purchases'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='buy'),
]
