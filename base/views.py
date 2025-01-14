from django.shortcuts import render
from .models import Category, Product

# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, "base/home.html", {'categories' : categories, 'products': products})


def shopping_cart(request):
    return render(request, "base/shopping_cart.html")
