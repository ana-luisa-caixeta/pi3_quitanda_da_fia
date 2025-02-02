from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Category, Product, ShoppingCart, CartItem

# Create your views here.
categories = Category.objects.all()
products = Product.objects.all()

def home(request):
    return render(request, "base/home.html", {'products': products})


@login_required(login_url='login')
def shopping_cart(request):
    # Recuperar o carrinho de compras do usuário logado
    cart = ShoppingCart.objects.filter(user=request.user, deleted_at__isnull=True).first()

    if not cart:
        # Se o carrinho não existir, renderizar a página com carrinho vazio
        return render(request, 'base/shopping_cart.html', {'cart': None, 'items': []})

    # Recuperar os itens do carrinho com o método select_related para otimizar o acesso ao produto
    items = cart.items.select_related('product')

    # Calcular o total do carrinho
    total = 0
    for item in items:
        total += item.product.price * item.quantity  # Multiplicando o preço pelo número de itens

    return render(request, 'base/shopping_cart.html', {'cart': cart, 'items': items, 'total': total})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart = ShoppingCart.objects.get_or_create(user=request.user, deleted_at__isnull=True)

        # Verifica se o item já existe no carrinho
        item, item_created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)

        if not item_created:
            # Atualiza a quantidade
            item.quantity += quantity
            item.save()

        return redirect('carrinho')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        # Busca o CartItem pelo ID
        cart_item = get_object_or_404(CartItem, id=item_id)

        if cart_item.quantity > 1:
            # Diminui a quantidade em 1
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # Se a quantidade for 1, remove o item completamente
            cart_item.delete()

        return redirect('carrinho')


def cadastro(request):
    if request.method == "GET": 
        return render(request, "registration/register.html")
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email).first()
        if user:
            messages.error(request, "Este email já está cadastrado.")
            return render(request, "registration/register.html")


        user = User.objects.filter(username=username).first()
        if user:
            messages.error(request, "Este usuário já está cadastrado.")
            return render(request, "registration/register.html")
        
        user  = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect("home")


def busca(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'results': results,
        'categories' : categories
    }

    return render(request, "base/search.html", context)


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='home')  # Redireciona usuários comuns
def edicao(request):
    return render(request, "base/edit.html")
