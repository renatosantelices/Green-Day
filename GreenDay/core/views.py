from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import PerfilForm

# Create your views here.

# -----------------------------
# Catálogo
# -----------------------------


def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'core/catalogo.html', {'productos': productos})

# -----------------------------
# Carrito
# -----------------------------

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtenemos el carrito de la sesión o lo creamos
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1  # si ya está, aumentamos cantidad
    else:
        carrito[str(producto_id)] = 1  # si no, agregamos con cantidad 1

    request.session['carrito'] = carrito  # guardamos en la sesión
    return redirect('catalogo')  # redirige al catálogo

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        producto.cantidad = cantidad
        producto.subtotal = producto.precio * cantidad
        total += producto.subtotal
        productos.append(producto)

    return render(request, 'core/carrito.html', {'productos': productos, 'total': total})


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')


# -----------------------------
# Pedidos
# -----------------------------

@login_required
def finalizar_pedido(request):
    carrito = request.session.get('carrito', {})

    if not carrito:
        return render(request, 'core/finalizar.html', {"mensaje": "Tu carrito está vacío."})

    # Crear el pedido
    pedido = Pedido.objects.create(total=0)
    total = 0

    # Crear los detalles
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        subtotal = producto.precio * cantidad
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            subtotal=subtotal
        )
        total += subtotal
        # Descontar del stock
        producto.stock -= cantidad
        producto.save()

    # Actualizar el total del pedido
    pedido.total = total
    pedido.save()

    # Vaciar carrito
    request.session['carrito'] = {}

    return render(request, 'core/finalizar.html', {"mensaje": "¡Gracias por tu compra!"})


@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user.cliente).order_by('-fecha')
    return render(request, 'core/historial_pedidos.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user.cliente)
    detalles = pedido.detalles.all()
    return render(request, 'core/detalle_pedido.html', {'pedido': pedido, 'detalles': detalles})

# -----------------------------
# Perfil
# -----------------------------

@login_required
def ver_perfil(request):
    cliente = request.user.cliente
    if request.method == "POST":
        form = PerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente ✅")
            return redirect('ver_perfil')
    else:
        form = PerfilForm(instance=cliente)
    return render(request, 'core/perfil.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('catalogo')