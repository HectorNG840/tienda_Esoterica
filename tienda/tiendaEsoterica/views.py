from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil, Producto, Categoria, User, Carrito, CarritoItem, Pedido, PedidoItem
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import PerfilUpdateForm
from .models import Perfil
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EnvioForm, PagoForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def inicio(request):
    categorias = Categoria.objects.all()

    query = request.GET.get('search', '').strip()
    categoria_id = request.GET.get('categoria', None)
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')

    productos = Producto.objects.all()
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if query:
        productos = productos.filter(nombre__icontains=query)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    return render(request, 'inicio.html', {
        'productos': productos,
        'categorias': categorias,
        'precio_min': precio_min,
        'precio_max': precio_max,
    })


@login_required
def perfil(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))  # Redirigir al panel de administración
    try:
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        # Si el perfil no existe, podrías redirigir al usuario a una página para crearlo o mostrar un error
        return redirect('crear_perfil')  # Ajusta esta ruta según tus necesidades
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
    if producto.cantidad < cantidad:
        return redirect('producto_detalle', pk=producto_id)
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
    producto.cantidad -= cantidad
    producto.save()
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

    producto.cantidad -= cantidad
    producto.save()
    
    return redirect('carrito')

def carrito_view(request):
    carrito_items = []
    total = 0
    gastos_envio = 0
    mensaje_gastos_envio = ""
    
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
    if total < 30:
        gastos_envio = 3
        mensaje_gastos_envio = "+ 3€ de gastos de envío."

    total_final = total + gastos_envio

    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total,
        'gastos_envio': gastos_envio,
        'total_final': total_final,
        'mensaje_gastos_envio': mensaje_gastos_envio,
    })

def resumen_pedido(request):
    carrito_items = []
    total = 0
    gastos_envio = 0
    mensaje_gastos_envio = ""
    
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
    
    if total < 30:
        gastos_envio = 3
        mensaje_gastos_envio = "+ 3€ de gastos de envio."
    total_final = total + gastos_envio
    
    if request.method == 'POST':
        envio_form = EnvioForm(request.POST)
        pago_form = PagoForm(request.POST)
        metodo_pago = request.POST.get('metodo_pago')
        
        if envio_form.is_valid() and (metodo_pago == 'contrareembolso' or pago_form.is_valid()):
            # Crear el pedido
            pedido = Pedido.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=envio_form.cleaned_data['email'],
                estado='P',
                direccion_envio=envio_form.cleaned_data['direccion_envio']
            )
            
            # Crear los ítems del pedido
            for item in carrito_items:
                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=item.producto if request.user.is_authenticated else item['producto'],
                    cantidad=item.cantidad if request.user.is_authenticated else item['cantidad']
                )
            
            # Limpiar el carrito después de procesar el pedido
            if request.user.is_authenticated:
                carrito.carritoitem_set.all().delete()  # Limpiar ítems del carrito
            else:
                request.session['carrito'] = {}  # Limpiar el carrito en la sesión
            
            # Enviar el ID de seguimiento por correo electrónico
            if not request.user.is_authenticated:

                customer_email = envio_form.cleaned_data['email']
                tracking_id = pedido.numero_seguimiento
                html_message = render_to_string('confirmacion_pedido.html', {
                    'product': ', '.join([f"{item.cantidad} x {item.producto.nombre}" for item in pedido.items.all()]),
                    'amount': f"${pedido.precio_total}",
                    'address': pedido.direccion_envio,
                    'tracking_id': tracking_id
                })
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to = customer_email
                send_mail(
                    'Confirmación de compra',
                    plain_message,
                    from_email,
                    [to],
                    html_message=html_message,
                    fail_silently=False,
                )
            
            return redirect('confirmacion_pedido', pedido_id=pedido.id)
    else:
        envio_form = EnvioForm()
        pago_form = PagoForm()
    
    return render(request, 'resumen_pedido.html', {
        'envio_form': envio_form,
        'pago_form': pago_form,
        'carrito_items': carrito_items,
        'total': total,
        'gastos_envio': gastos_envio,
        'total_final': total_final,
        'mensaje_gastos_envio': mensaje_gastos_envio,
    })


def seguimiento_pedido(request):
    pedido = None  # Inicializa la variable del pedido como None
    searched = False  # Indica si se ha realizado una búsqueda

    if request.method == 'POST':
        searched = True  # El usuario hizo clic en buscar
        tracking_id = request.POST.get('tracking_id')
        try:
            pedido = Pedido.objects.get(numero_seguimiento=tracking_id)
        except Pedido.DoesNotExist:
            pedido = None  # Pedido no encontrado

    return render(request, 'seguimiento_pedido.html', {'pedido': pedido, 'searched': searched})

    
def confirmacion_pedido(request, pedido_id):
    # Obtener el pedido del usuario
    if request.user.is_authenticated:
     pedido = get_object_or_404(Pedido, id=pedido_id, user=request.user)
    else:
        pedido = get_object_or_404(Pedido, id=pedido_id)

    # Extraer los datos necesarios del pedido
    customer_email = pedido.email
    product = ', '.join([f"{item.cantidad} x {item.producto.nombre}" for item in pedido.items.all()])
    amount = f"${pedido.precio_total}"
    address = pedido.direccion_envio
    tracking_id = pedido.numero_seguimiento

    # Renderizar la plantilla HTML
    html_message = render_to_string('confirmacion_pedido.html', {
        'product': product,
        'amount': amount,
        'address': address,
        'tracking_id': tracking_id
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = customer_email

    # Enviar el correo
    send_mail(
        'Confirmación de compra',
        plain_message,
        from_email,
        [to],
        html_message=html_message,
        fail_silently=False,
    )

    return render(request, 'confirmacion_pedido.html', {
        'product': product,
        'amount': amount,
        'address': address,
        'tracking_id': tracking_id
    })

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).prefetch_related('items__producto')
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})

