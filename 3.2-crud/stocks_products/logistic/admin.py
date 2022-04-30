from django.contrib import admin

# Register your models here.
from logistic.models import Product, Stock, StockProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    #list_filter = ['brand', 'model']


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 0


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']
    #list_filter = ['brand', 'model']
    inlines = [StockProductInline]


