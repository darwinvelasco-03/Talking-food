from .models import Usuario,  Historial, Comentarios, ListaFavoritos, Alimento, Restaurante, RegistroUsuario
from rest_framework import viewsets, permissions
from .serializers import UsuarioSerializer, HistorialSerializer, ComentariosSerializer, ListaFavoritosSerializer, AlimentoSerializer, RestauranteSerializer, RegistroUsuarioSerializer
from django_filters.rest_framework import DjangoFilterBackend

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsuarioSerializer
   
    

class HistorialViewSet(viewsets.ModelViewSet):
    queryset = Historial.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = HistorialSerializer

class ComentariosViewSet(viewsets.ModelViewSet):
    queryset = Comentarios.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ComentariosSerializer

class ListaFavoritosViewSet(viewsets.ModelViewSet):
    queryset = ListaFavoritos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ListaFavoritosSerializer

class AlimentoViewSet(viewsets.ModelViewSet):
    queryset = Alimento.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AlimentoSerializer

class RestauranteViewSet(viewsets.ModelViewSet):
    queryset = Restaurante.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RestauranteSerializer

class RegistroUsuarioViewSet(viewsets.ModelViewSet):
    queryset = RegistroUsuario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistroUsuarioSerializer


