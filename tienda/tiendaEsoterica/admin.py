from django.contrib import admin
from .models import Perfil, Categoria, Producto, Pedido, PedidoItem

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fecha_pedido', 'direccion_envio', 'total_productos', 'estado')
    inlines = [PedidoItemInline]

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto)
admin.site.register(Categoria)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'fecha_nacimiento', 'preferencias_esotericas']
