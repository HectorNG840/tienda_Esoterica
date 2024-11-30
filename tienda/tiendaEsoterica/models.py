import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Añadir esta línea
from django.dispatch import receiver
from django.db.models.signals import post_save

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    preferencias_esotericas = models.TextField(blank=True, null=True)  # Asegúrate de definir este campo si es necesario

    def __str__(self):
        return self.user.username



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    cantidad = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pedido'),
        ('C', 'Enviado'),
        ('E', 'Entregado'),
        ('X', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    productos = models.ManyToManyField(Producto, related_name='pedidos')
    fecha_pedido = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    numero_seguimiento = models.CharField(max_length=100, blank=True, null=True, unique=True)
    fecha_actualizacion_estado = models.DateTimeField(auto_now=True)

    @property
    def precio_total(self):
        return sum(producto.precio for producto in self.productos.all())

    def save(self, *args, **kwargs):
        if not self.direccion_envio and self.user.perfil.direccion:
            self.direccion_envio = self.user.perfil.direccion
        if not self.numero_seguimiento:
            self.numero_seguimiento = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.fecha_actualizacion_estado = timezone.now()
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"
    
class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoItem')

    def __str__(self):
        return f"Carrito de {self.user.username}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created and not instance.is_staff:  # Crear perfiles solo para usuarios normales
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):  # Guardar perfil si existe
        instance.perfil.save()