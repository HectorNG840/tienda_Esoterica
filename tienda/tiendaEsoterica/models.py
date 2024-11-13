from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    preferencias_esotericas = models.TextField(blank=True, help_text="Intereses o preferencias en productos esotéricos")
    historial_compras = models.TextField(blank=True, help_text="Historial de compras en la tienda esotérica")

    def __str__(self):
        return f"Perfil de {self.user.username}"
