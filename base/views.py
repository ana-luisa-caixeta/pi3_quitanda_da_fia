from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "base/base.html")


def cart(request):
    return render(request, "base/cart.html")