from django.contrib import admin

from orders.models import Discount, Order


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'modified')
    list_display_links = ('id',)
    search_fields = ('modified',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified')
    list_display_links = ('id',)
    search_fields = ('id', 'created')
