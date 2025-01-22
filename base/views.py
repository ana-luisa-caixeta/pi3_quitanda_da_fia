from django.shortcuts import render
from .models import Category, Product

# Create your views here.
categories = Category.objects.all()
products = Product.objects.all()

def home(request):
    return render(request, "base/home.html", {'categories' : categories, 'products': products})


def shopping_cart(request):
    return render(request, "base/shopping_cart.html", {'categories' : categories})


def login(request):
    return render(request, "base/login.html", {'categories' : categories})


def cadastro(request):
    return render(request, "base/register.html", {'categories' : categories})


def busca(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'results': results,
        'categories' : categories
    }

    return render(request, "base/search.html", context)
