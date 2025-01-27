from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, ShoppingCart, CartItem

# Create your views here.
categories = Category.objects.all()
products = Product.objects.all()

def home(request):
    return render(request, "base/home.html", {'categories' : categories, 'products': products})


from django.shortcuts import render
from .models import ShoppingCart, CartItem  # Certifique-se de importar os modelos corretos


def shopping_cart(request):
    # Recuperar o carrinho de compras do usuário logado
    cart = ShoppingCart.objects.filter(user=request.user, deleted_at__isnull=True).first()

    if not cart:
        # Se o carrinho não existir, renderizar a página com carrinho vazio
        return render(request, 'base/shopping_cart.html', {'cart': None, 'items': [], 'categories': categories})

    # Recuperar os itens do carrinho com o método select_related para otimizar o acesso ao produto
    items = cart.items.select_related('product')

    # Calcular o total do carrinho
    total = 0
    for item in items:
        total += item.product.price * item.quantity  # Multiplicando o preço pelo número de itens

    return render(request, 'base/shopping_cart.html', {'cart': cart, 'items': items, 'total': total, 'categories': categories})


def add_to_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart, created = ShoppingCart.objects.get_or_create(user=request.user, deleted_at__isnull=True)

        # Verifica se o item já existe no carrinho
        item, item_created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)

        if not item_created:
            # Atualiza a quantidade
            item.quantity += quantity
            item.save()

        return redirect('carrinho')


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
