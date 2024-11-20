from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tiendaEsoterica import views
from tiendaEsoterica.admin import admin

urlpatterns = [
        # Página de inicio que se mostrará después de iniciar sesión
    path('', views.inicio, name='inicio'),
    # URL para el inicio de sesión
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    
    # URL para el cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),

    path('perfil/', views.perfil, name='perfil'),
    
    # URL para el registro
    path('register/', views.register, name='register'),

    
    # Otras rutas, como detalles de productos
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
