from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tiendaEsoterica import views
from tiendaEsoterica.admin import admin

urlpatterns = [
    # URL para el inicio de sesión
    path('login/', auth_views.LoginView.as_view(template_name='tiendaEsoterica/login.html'), name='login'),
    
    # URL para el cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),
    
    # URL para el registro
    path('register/', views.register, name='register'),

    # Redirige la URL raíz a la página de inicio de sesión
    path('', auth_views.LoginView.as_view(template_name='tiendaEsoterica/login.html'), name='login'),
    
    # Página de inicio que se mostrará después de iniciar sesión
    path('inicio/', views.inicio, name='inicio'),
    
    # Otras rutas, como detalles de productos
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)