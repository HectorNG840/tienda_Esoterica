from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil

from django.shortcuts import render

def home(request):
    return render(request, 'tiendaEsoterica/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user)  # Crear un perfil vacío para el nuevo usuario
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('home')  # Redirigir a la página principal (ajusta esta URL según tu proyecto)
    else:
        form = UserCreationForm()
    return render(request, 'tiendaEsoterica/register.html', {'form': form})
