from django.urls import path
from django.contrib.auth import views as auth_views
from tiendaEsoterica import views

from django.urls import path
from tiendaEsoterica import views


urlpatterns = [
    # URL para el inicio de sesión
    path('login/', auth_views.LoginView.as_view(template_name='tiendaEsoterica/login.html'), name='login'),
    
    # URL para el cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # URL para el registro
    path('register/', views.register, name='register'),

    path('', views.home, name='home'),  # Página principal
    path('login/', auth_views.LoginView.as_view(template_name='tiendaEsoterica/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),

]
