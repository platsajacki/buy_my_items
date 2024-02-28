from django.urls import path

from items.views import ItemList

app_name = 'items'

urlpatterns = [
    path('', ItemList.as_view(), name='index'),
]
