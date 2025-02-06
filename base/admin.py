from django.contrib import admin
from .models import Category, Product, OrderInformation, ShoppingCart, CartItem  # Substitua pelos seus modelos


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')


# Registrar modelos
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderInformation)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
