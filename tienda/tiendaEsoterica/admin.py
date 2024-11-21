from django.contrib import admin
from .models import Perfil
from .models import Producto, Categoria

admin.site.register(Producto)
admin.site.register(Categoria)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'fecha_nacimiento', 'preferencias_esotericas']
