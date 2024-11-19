from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto, Categoria


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
            'username': 'newuser2@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        }
        # Realizar una solicitud POST a la vista de registro
        response = self.client.post(reverse('register'), register_data)
        
        # Verificar que la redirección sea a la página de perfil
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('perfil'))
        

    def test_register_with_invalid_data(self):
        # Datos de registro inválidos (contraseñas no coinciden)
        register_data = {
            'username': 'newuser',
            'password1': 'Testpassword123',
            'password2': 'Differentpassword'
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