
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil
from .models import Perfil
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria


def inicio(request):
    productos = Producto.objects.all()  # Trae todos los productos
    return render(request, 'tiendaEsoterica/inicio.html', {'productos': productos})

@login_required
def perfil(request):
    return render(request, 'tiendaEsoterica/perfil.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user)  # Crear un perfil vacío para el nuevo usuario
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('perfil')  # Redirigir a la página de perfil
            user = form.save()
            Perfil.objects.create(user=user)  # Crear un perfil vacío para el nuevo usuario
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('perfil')  # Redirigir a la página de perfil
    else:
        form = UserCreationForm()
        form = UserCreationForm()
    return render(request, 'tiendaEsoterica/register.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('')  # Redirige a la página raíz después de iniciar sesión
    else:
        form = AuthenticationForm()
        form = AuthenticationForm()
    return render(request, 'tiendaEsoterica/login.html', {'form': form})
    
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'tiendaEsoterica/producto_detalle.html', {'producto': producto})
