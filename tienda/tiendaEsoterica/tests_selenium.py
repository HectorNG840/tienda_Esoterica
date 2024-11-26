# FILE: tiendaEsoterica/tests_selenium.py

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from .models import Producto, Categoria
from django.contrib.auth.models import User

class SeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
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
    
    def tearDown(self):
        self.driver.quit()
    
    def test_add_to_cart_and_proceed_to_payment(self):

        self.driver.get(self.live_server_url + reverse('login'))
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword')
        self.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
        

        self.driver.get(self.live_server_url + reverse('producto_detalle', args=[self.producto1.id]))
        self.driver.find_element(By.NAME, 'cantidad').send_keys('1')
        self.driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()
        
        self.driver.get(self.live_server_url + reverse('producto_detalle', args=[self.producto2.id]))
        self.driver.find_element(By.NAME, 'cantidad').send_keys('2')
        self.driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()
        

        self.driver.get(self.live_server_url + reverse('carrito'))
        self.assertIn('Producto 1', self.driver.page_source)
        self.assertIn('Producto 2', self.driver.page_source)
        

        self.driver.get(self.live_server_url + reverse('resumen_pedido'))
        self.assertIn('Resumen del Pedido', self.driver.page_source)
        
        
        self.driver.find_element(By.NAME, 'nombre').send_keys('Test User')
        self.driver.find_element(By.NAME, 'direccion').send_keys('123 Test St')
        self.driver.find_element(By.NAME, 'ciudad').send_keys('Test City')
        self.driver.find_element(By.NAME, 'codigo_postal').send_keys('12345')
        self.driver.find_element(By.NAME, 'pais').send_keys('Test Country')
        self.driver.find_element(By.NAME, 'numero_tarjeta').send_keys('4111111111111111')
        self.driver.find_element(By.NAME, 'fecha_expiracion').send_keys('12/23')
        self.driver.find_element(By.NAME, 'cvv').send_keys('123')
        self.driver.find_element(By.NAME, 'nombre_titular').send_keys('Test User')
        self.driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()
        