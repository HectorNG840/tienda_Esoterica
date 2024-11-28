
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil, Producto, Categoria, User, Carrito, CarritoItem, Pedido
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import PerfilUpdateForm
from .models import Perfil
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EnvioForm, PagoForm
from django.shortcuts import render

def inicio(request):
    categorias = Categoria.objects.all()

    query = request.GET.get('search', '').strip()
    categoria_id = request.GET.get('categoria', None)

    productos = Producto.objects.all()
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if query:
        productos = productos.filter(nombre__icontains=query)

    return render(request, 'inicio.html', {
        'productos': productos,
        'categorias': categorias,
    })


@login_required
def perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    return render(request, 'perfil.html', {'perfil': perfil})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],
            )
            user.save()

            Perfil.objects.create(
                user=user,
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion'],
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                codigo_postal=form.cleaned_data['codigo_postal'],
            )

            login(request, user)

            return redirect('inicio')
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
            form.save()  # El formulario ya maneja el valor de fecha_nacimiento
            return redirect('perfil')
    else:
        form = PerfilUpdateForm(instance=perfil)
    return render(request, 'editar_perfil.html', {'form': form})


def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(user=request.user)
    else:
        carrito = request.session.get('carrito', {})
        if str(producto_id) in carrito:
            carrito[str(producto_id)] += cantidad
        else:
            carrito[str(producto_id)] = cantidad
        request.session['carrito'] = carrito
        return redirect('carrito')
    
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        carrito_item.cantidad += cantidad
    else:
        carrito_item.cantidad = cantidad
    carrito_item.save()
    return redirect('carrito')

def remove_from_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', -1))
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, user=request.user)
        carrito_item = get_object_or_404(CarritoItem, carrito=carrito, producto=producto)
        if carrito_item.cantidad > 1:
            carrito_item.cantidad += cantidad
            carrito_item.save()
        else:
            carrito_item.delete()
    else:
        carrito = request.session.get('carrito', {})
        if str(producto_id) in carrito:
            if carrito[str(producto_id)] > 1:
                carrito[str(producto_id)] += cantidad
            else:
                del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('carrito')

def carrito_view(request):
    carrito_items = []
    total = 0
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(user=request.user)
        carrito_items = carrito.carritoitem_set.all()
        total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    else:
        carrito = request.session.get('carrito', {})
        for producto_id, cantidad in carrito.items():
            producto = get_object_or_404(Producto, id=producto_id)
            carrito_items.append({
                'producto': producto,
                'cantidad': cantidad,
                'total': producto.precio * cantidad
            })
            total += producto.precio * cantidad
    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})

def resumen_pedido(request):
    carrito_items = []
    total = 0
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(user=request.user)
        carrito_items = carrito.carritoitem_set.all()
        total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    else:
        carrito = request.session.get('carrito', {})
        for producto_id, cantidad in carrito.items():
            producto = get_object_or_404(Producto, id=producto_id)
            carrito_items.append({
                'producto': producto,
                'cantidad': cantidad,
                'total': producto.precio * cantidad
            })
            total += producto.precio * cantidad
    
    if request.method == 'POST':
        envio_form = EnvioForm(request.POST)
        pago_form = PagoForm(request.POST)
        if envio_form.is_valid() and pago_form.is_valid():
            pedido = Pedido.objects.create(
                user=request.user,
                estado='P',
                direccion_envio=envio_form.cleaned_data['direccion_envio']
            )
            for item in carrito_items:
                pedido.productos.add(item.producto)
            pedido.save()
            if request.user.is_authenticated:
                carrito.carritoitem_set.all().delete()
            else:
                request.session['carrito'] = {}
            return redirect('confirmacion_pedido')
    else:
        envio_form = EnvioForm()
        pago_form = PagoForm()
    
    return render(request, 'resumen_pedido.html', {'carrito_items': carrito_items, 'total': total, 'envio_form': envio_form, 'pago_form': pago_form})

def confirmacion_pedido(request):
    return render(request, 'confirmacion_pedido.html')

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user)
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})