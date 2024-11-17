from django.contrib import admin
from .models import Perfil
from .models import Producto, Categoria

admin.site.register(Perfil)
admin.site.register(Producto)
admin.site.register(Categoria)

