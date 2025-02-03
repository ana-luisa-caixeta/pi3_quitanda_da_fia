from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from .models import Category, Product, ShoppingCart, CartItem, OrderInformation
import urllib.parse

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

        with transaction.atomic():  # Garante que tudo ocorre sem erros parciais
            cart, created = ShoppingCart.objects.get_or_create(user=request.user, deleted_at__isnull=True)

            product = get_object_or_404(Product, id=product_id)  # Garante que o produto existe

            item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not item_created:
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


def generate_whatsapp_message(order):
    # Formatar a mensagem
    message = f"📦 Tipo de serviço: {order.delivery}\n"
    message += f"📍 Endereço: {order.address if order.delivery == 'Entrega' else 'https://g.co/kgs/HA98aZi'}\n\n"
    message += f"✨ Nome: {order.name}\n"
    message += f"📱 Telefone: {order.tel_number}\n\n"
    message += "📋 Pedido:\n"

    # Buscar os itens que pertencem ao carrinho deste pedido
    for item in order.cart.items.all():
        message += f"{item.quantity}x {item.product.name} - R${item.product.price * item.quantity:.2f}\n"

    message += "\n🧾 Custos\n"
    message += f"🛍️ Total dos produtos: R${order.total:.2f}\n"
    message += "🚚 Valor da entrega: GRÁTIS\n"
    message += f"💸 Total a pagar: R${order.total:.2f}\n"
    message += f"💰 Tipo de pagamento: {order.get_payment_display()}\n\n"
    message += "🕒 Após enviar o pedido, aguarde que já iremos lhe atender."

    return message


@login_required(login_url='login')
def checkout(request):
    # Verificar se o carrinho está vazio
    cart = ShoppingCart.objects.filter(user=request.user, deleted_at__isnull=True).first()
    if not cart or not cart.items.exists():
        return redirect('shopping_cart')  # Redireciona de volta caso o carrinho esteja vazio

    # Se o formulário de pedido for enviado (POST)
    if request.method == "POST":
        # Extrair os dados do formulário
        name = request.POST['name']
        tel_number = request.POST['tel_number']
        payment = request.POST['payment']
        delivery = request.POST['delivery']
        address = request.POST.get('address', '')  # Address pode ser nulo
        total = cart.get_total_price()

        # Criar uma instância do pedido
        order = OrderInformation.objects.create(
            cart=cart,
            name=name,
            tel_number=tel_number,
            payment=payment,
            delivery=delivery,
            address=address,
            total=total
        )

        # Gerar a mensagem do WhatsApp com os itens do pedido
        message = generate_whatsapp_message(order)

        whatsapp_url = f"https://api.whatsapp.com/send?phone=5561999038103&text={message}"

        try:
            # Obter o carrinho ativo (não deletado)
            cart = ShoppingCart.objects.get(user=request.user, deleted_at__isnull=True)
            cart.deleted_at = timezone.now()  # Marca o carrinho como deletado
            cart.save()
        except ShoppingCart.DoesNotExist:
            # Caso não haja um carrinho ativo, não faz nada
            pass

        new_cart = ShoppingCart.objects.create(user=request.user)

        return redirect(whatsapp_url)

    return render(request, 'base/shopping_cart.html', {'cart': cart})
