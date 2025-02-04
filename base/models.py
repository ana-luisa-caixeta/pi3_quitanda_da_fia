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
    
    def get_total_price(self):
        # Calcula o preço total do carrinho somando o preço de todos os itens
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Relacionado ao produto
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} no carrinho"


class OrderInformation(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Cartão'),
        ('cash', 'Dinheiro')
    ]
    
    DELIVERY_CHOICES = [
        ('pickup', 'Retirada na loja'),
        ('delivery', 'Entrega')
    ]

    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tel_number = models.CharField(max_length=15)
    payment = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    delivery = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    address = models.TextField(blank=True, null=True)  # Pode ser nulo caso seja retirada na loja
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.name} - R${self.total}"


"""FAZENDO FUNCIONAR FORM DE ADD PRODUTO"""
class ProductUm(models.Model): 
    UNITS = [
        ("Kg", "Kg"),
        ("Unidade", "Unidade"),
    ]
    
    CATEGORIES = [
        ("Carne", "Carne"),
        ("Frutas", "Frutas"),
        ("Verduras", "Verduras"),
        ("Legumes", "Legumes"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNITS)  # 🔹 Usando a constante UNITS
    category = models.CharField(max_length=20, choices=CATEGORIES)  # 🔹 Usando a constante CATEGORIES
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name