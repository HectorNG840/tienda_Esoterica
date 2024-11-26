from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto, Categoria, Carrito, CarritoItem


class LoginTestCase(TestCase):
     def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpassword')
     def test_login_with_valid_credentials(self):
        # Datos de login válidos
        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        # Realizar una solicitud POST a la vista de login
        response = self.client.post(reverse('login'), login_data)
        
        # Verificar que la redirección sea a la página de inicio
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inicio'))
    
     def test_login_with_invalid_credentials(self):
        # Datos de login inválidos
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        # Realizar una solicitud POST a la vista de login
        response = self.client.post(reverse('login'), login_data)
        
        # Verificar que la página de login se recargue con un error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.")

class RegisterTestCase(TestCase):
    def test_register_with_valid_data(self):
        # Datos de registro válidos
        register_data = {
            'first_name':'Prueba',
            'last_name':'Prueba',
            'email':'testuser@example.com',
            'telefono':'123908674',
            'direccion':'Reina Mercedes',
            'fecha_nacimiento':'21/10/2002',
            'codigo_postal':'41012',
            'password1':'Contraseñaprueba123',
            'password2':'Contraseñaprueba123'
        }
        # Realizar una solicitud POST a la vista de registro
        response = self.client.post(reverse('register'), register_data)
        
        # Verificar que la redirección sea a la página de perfil
        self.assertEqual(response.status_code, 302)
        

    def test_register_with_invalid_data(self):
        # Datos de registro inválidos (contraseñas no coinciden)
        register_data = {
            'first_name':'Prueba',
            'last_name':'Prueba',
            'username':'testuser@example.com',
            'telefono':'123908674',
            'direccion':'Reina Mercedes',
            'fecha_nacimiento':'21/10/2002',
            'codigo_postal':'41012',
            'password1':'Contraseñaprueba123',
            'password2':'contraseñaprueba123'
        }
        # Realizar una solicitud POST a la vista de registro
        response = self.client.post(reverse('register'), register_data)
        
        # Verificar que la página de registro se recargue con un error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Los dos campos de contraseña no coinciden.")

class InicioTestCase(TestCase):
    def setUp(self):
        # Crear una categoría y algunos productos para las pruebas
        self.categoria = Categoria.objects.create(nombre='Categoría de Prueba')
        self.producto1 = Producto.objects.create(
            nombre='Producto 1',
            descripcion='Descripción del Producto 1',
            precio=10.0,
            imagen='tienda\media\productos\images.jpg',
            categoria=self.categoria
        )
        self.producto2 = Producto.objects.create(
            nombre='Producto 2',
            descripcion='Descripción del Producto 2',
            precio=20.0,
            imagen='tienda\media\productos\images.jpg',
            categoria=self.categoria
        )

    def test_inicio_view(self):
        # Realizar una solicitud GET a la vista de inicio
        response = self.client.get(reverse('inicio'))
        
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verificar que los productos se muestran en la página
        self.assertContains(response, 'Producto 1')
        self.assertContains(response, 'Producto 2')
        self.assertContains(response, 'Descripción del Producto 1')
        self.assertContains(response, 'Descripción del Producto 2')
        self.assertContains(response, 'Categoría de Prueba')

class CarritoTestCase(TestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Crear una categoría y algunos productos para las pruebas
        self.categoria = Categoria.objects.create(nombre='Categoría de Prueba')
        self.producto1 = Producto.objects.create(
            nombre='Producto 1',
            descripcion='Descripción del Producto 1',
            precio=10.0,
            imagen='path/to/image1.jpg',
            categoria=self.categoria
        )
        self.producto2 = Producto.objects.create(
            nombre='Producto 2',
            descripcion='Descripción del Producto 2',
            precio=20.0,
            imagen='path/to/image2.jpg',
            categoria=self.categoria
        )
    
    def test_add_to_cart_and_proceed_to_payment(self):
        # Iniciar sesión
        self.client.login(username='testuser', password='testpassword')
        
        # Añadir productos al carrito
        response = self.client.post(reverse('add_to_cart', args=[self.producto1.id]), {'cantidad': 1})
        self.assertEqual(response.status_code, 302)  # Redirección después de añadir al carrito
        
        response = self.client.post(reverse('add_to_cart', args=[self.producto2.id]), {'cantidad': 2})
        self.assertEqual(response.status_code, 302)  # Redirección después de añadir al carrito
        
        # Verificar que los productos están en el carrito
        carrito = Carrito.objects.get(user=self.user)
        carrito_items = CarritoItem.objects.filter(carrito=carrito)
        self.assertEqual(carrito_items.count(), 2)
        self.assertEqual(carrito_items.get(producto=self.producto1).cantidad, 1)
        self.assertEqual(carrito_items.get(producto=self.producto2).cantidad, 2)
        
        # Proceder al pago
        response = self.client.get(reverse('resumen_pedido'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resumen del Pedido')
        
        # Enviar datos de envío y pago
        response = self.client.post(reverse('resumen_pedido'), {
            'nombre': 'Test User',
            'direccion': '123 Test St',
            'ciudad': 'Test City',
            'codigo_postal': '12345',
            'pais': 'Test Country',
            'numero_tarjeta': '4111111111111111',
            'fecha_expiracion': '12/23',
            'cvv': '123',
            'nombre_titular': 'Test User'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de confirmar el pedido
        self.assertRedirects(response, reverse('confirmacion_pedido'))