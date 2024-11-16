from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

# Create your views here.
def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})
