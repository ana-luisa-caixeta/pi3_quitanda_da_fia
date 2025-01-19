from django.shortcuts import render
from .models import Category, Product

# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, "base/home.html", {'categories' : categories, 'products': products})


def shopping_cart(request):
    return render(request, "base/shopping_cart.html")


def login(request):
    return render(request, "base/login.html")


def cadastro(request):
    return render(request, "base/register.html")


def busca(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'results': results,
    }

    return render(request, "base/search.html", context)
