from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil, Producto, Categoria
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def inicio(request):
    return render(request, 'tiendaEsoterica/inicio.html')


def home(request):
    return render(request, 'tiendaEsoterica/home.html')


@login_required
def perfil(request):
    return render(request, 'tiendaEsoterica/perfil.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crear un nuevo usuario
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            user.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tiendaEsoterica/register.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'tiendaEsoterica/login.html', {'form': form})


'''
# Create your views here.
def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})
'''


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})
