from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'total_value')
    list_filter = ('quantity',)
    search_fields = ('name',)
    actions = ['make_free']

    def make_free(self, request, queryset):
        queryset.update(price=0)
    make_free.short_description = "Make products free"
