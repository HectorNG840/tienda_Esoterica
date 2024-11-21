from django.contrib import admin
from .models import Perfil, Categoria, Producto, Pedido


admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Pedido)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'fecha_nacimiento', 'preferencias_esotericas']
