"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from base.views import home, shopping_cart, login, cadastro, busca, add_to_cart, remove_from_cart, edicao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('carrinho/', shopping_cart, name='carrinho'),
    path('cart/add/<str:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('busca/', busca, name='busca'),
    path('edicao/', edicao, name='edicao'),
]
