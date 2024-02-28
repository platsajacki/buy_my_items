from django.contrib import admin

from items.models import Item, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'tax')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_display_links = ('name',)
    search_fields = ('name',)
