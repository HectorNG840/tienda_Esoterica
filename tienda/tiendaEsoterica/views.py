
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

@login_required
def perfil(request):
    return render(request, 'tiendaEsoterica/perfil.html')


def home(request):
    return render(request, 'tiendaEsoterica/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user)  # Crear un perfil vacío para el nuevo usuario
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('perfil')  # Redirigir a la página de perfil
    else:
        form = UserCreationForm()
    return render(request, 'tiendaEsoterica/register.html', {'form': form})



# Create your views here.
def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})

