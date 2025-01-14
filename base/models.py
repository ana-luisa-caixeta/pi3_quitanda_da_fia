from django.db import models
from uuid import uuid4

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
