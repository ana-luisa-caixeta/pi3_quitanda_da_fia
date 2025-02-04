from django import forms
from .models import ProductUm

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductUm
        fields = ['name', 'description', 'price', 'unit', 'category', 'image_url']