from django.db import models
from uuid import uuid4
import uuid

class Category(models.Model):
    id = models.CharField(
        max_length=50, 
        primary_key=True, 
        default=uuid4, 
        editable=False
    )
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_by = models.CharField(max_length=100, null=False)


class Product(models.Model):
    UNITS = (
        ("unidade", "Unidade"),
        ("kg", "Kg"),
    )

    id = models.CharField(
        max_length=50, 
        primary_key=True, 
        editable=True
    )
    name = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    price = models.FloatField(null=False)
    unit = models.CharField(
        max_length=50,
        choices=UNITS
    )
    image = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_by = models.CharField(max_length=100, null=True, blank=True)


class ShoppingCart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Relacionado ao usuário
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Carrinho de {self.user.username}"
    

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Relacionado ao produto
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} no carrinho"