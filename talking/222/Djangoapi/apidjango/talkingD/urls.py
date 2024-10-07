from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from .views import *


urlpatterns = [
    path('iniciar-sesion/', views.iniciarSesion),
    path('registro/', views.registro),
    path('perfil/', views.perfil),
    path('perfil/actualizar/', views.actualizarPerfil, name='actualizar-perfil'),
    path('platos/agregar/', views.agregarPlato, name='agregar-plato'),
    path('platos/', views.listarPlatos, name='listar-platos'),
    path('usuarios/', views.lista_user, name='lista_user'),
    path('eliminar/usuario/<int:pk>/', views.eliminar_usuarios, name="eliminar_usuarios"),
    path('filtrar/', views.filtrar_platos, name="filtrar_productos"),
    path('plato/<int:plato_id>/comentarios/', agregar_comentario, name='agregar_comentario'),
    path('comentarios/', ver_comentarios, name='ver_comentarios'),
    path('actualizar/usuarios/<int:pk>/', views.actualizar_Usuario, name="actualizar_Usuario"),
    path('<int:plato_id>/comentarios/', ver_comentarios, name='comentario-list'),
]