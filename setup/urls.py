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
from base.views import home, shopping_cart, cadastro, busca, add_to_cart, remove_from_cart, edicao, checkout, create_product, admin_config_page, buscar_produto_edicao, delete_product

urlpatterns = [
 path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('carrinho/', shopping_cart, name='carrinho'),
    path('cart/add/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('busca/', busca, name='busca'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
    path('checkout/', checkout, name='checkout'),
    path('admin_config_page/', admin_config_page, name='admin_config_page'),
    path("produto/novo/", create_product, name="create_product"),
    path('produto/editar/', edicao, name='edit_product'),
    path("produto/editar/<int:id>/", edicao, name="edit_product"),
    path('produto/buscar/', buscar_produto_edicao, name='buscar_produto_edicao'),
    path('produto/excluir/<int:id>/', delete_product, name='delete_product'),
]
