
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil, Producto, Categoria, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import PerfilUpdateForm
from .models import Perfil


def inicio(request):
    productos = Producto.objects.all()  # Trae todos los productos
    return render(request, 'inicio.html', {'productos': productos})


@login_required
def perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    return render(request, 'perfil.html', {'perfil': perfil})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crear usuario
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],
            )
            user.save()
            
            # Crear perfil
            Perfil.objects.create(
                user=user,
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion'],
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                codigo_postal=form.cleaned_data['codigo_postal'],
            )
            
            # Redirigir al perfil
            return redirect('perfil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})

@login_required
def editar_perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    if request.method == 'POST':
        form = PerfilUpdateForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirigir al perfil después de guardar los cambios
    else:
        form = PerfilUpdateForm(instance=perfil)
    return render(request, 'editar_perfil.html', {'form': form})