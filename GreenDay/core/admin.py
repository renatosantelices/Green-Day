from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    search_fields = ('nombre',)

@admin.register(Invernadero)
class InvernaderoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono',)
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion', 'telefono')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente__user__username',)

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad')

