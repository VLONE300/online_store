from django.contrib import admin
from catalog.models import Category, Product, CashBack, Discount, Order, Promocode, ProductImage, Seller


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'price')
    search_fields = ('article', 'name', 'category__name')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Seller)
admin.site.register(CashBack)
admin.site.register(Order)
admin.site.register(Promocode)
admin.site.register(ProductImage)
