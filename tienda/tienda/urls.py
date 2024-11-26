from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tiendaEsoterica import views
from tiendaEsoterica.admin import admin
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
        # Página de inicio que se mostrará después de iniciar sesión
    path('', views.inicio, name='inicio'),  # Página principal
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('admin/', admin.site.urls), 
    # Otras rutas, como detalles de productos
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    
    path('add_to_cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:producto_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('resumen_pedido/', views.resumen_pedido, name='resumen_pedido'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
