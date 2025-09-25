from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver 

class Invernadero(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la planta
    descripcion = models.TextField(blank=True, null=True)  # Opcional
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Ej: 99999999.99
    stock = models.PositiveIntegerField(default=0)  # Cantidad disponible
    invernadero = models.ForeignKey(Invernadero, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre



class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=50)   
    apellido = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    else:
        instance.perfil.save()


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('C', 'Completado'),
        ('A', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        'Cliente', 
        on_delete=models.CASCADE, 
        related_name='pedidos'
    )
    productos = models.ManyToManyField(
        'Producto', 
        through='DetallePedido'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=1, 
        choices=ESTADO_CHOICES, 
        default='P'
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )

    def __str__(self):
        if hasattr(self.cliente, 'user'):
            return f"Pedido {self.id} - {self.cliente.user.username}"
        return f"Pedido {self.id} - Cliente {self.cliente.id}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        'Pedido', 
        on_delete=models.CASCADE, 
        related_name='detalles'
    )
    producto = models.ForeignKey(
        'Producto', 
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente antes de guardar
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"



@receiver(post_save, sender=User)
def crear_cliente(sender, instance, created, **kwargs):
    if created:
        # Solo si el cliente no existe todavía
        from core.models import Cliente
        if not hasattr(instance, 'cliente'):
            Cliente.objects.create(user=instance, direccion="Pendiente", telefono="Pendiente")
