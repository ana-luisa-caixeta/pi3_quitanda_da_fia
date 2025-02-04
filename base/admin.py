from django.contrib import admin
from .models import Category, Product, ProductUm

admin.site.register(Category)
admin.site.register(Product)

@admin.register(ProductUm)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit')  # 🔹 Define colunas visíveis
    search_fields = ('name', 'category')  # 🔹 Adiciona barra de busca
    list_filter = ('category', 'unit')  # 🔹 Adiciona filtros laterais
