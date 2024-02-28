from django.urls import path

from items.views import ItemDetail, ItemList

app_name = 'items'

urlpatterns = [
    path('', ItemList.as_view(), name='index'),
    path('<int:pk>/', ItemDetail.as_view(), name='detail'),
]
