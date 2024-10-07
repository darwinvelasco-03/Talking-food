from django.shortcuts import render
from warnings import filters
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import *
from .filters import *

from django.shortcuts import get_object_or_404
from . models import Usuarios, Platos, Comentarios
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def iniciarSesion(request):
    user = get_object_or_404(Usuarios, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuariosSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    serializer = UsuariosSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user  = Usuarios.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    serializer = UsuariosSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def agregarPlato(request):
    serializer = PlatosSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def listarPlatos(request):
    platos = Platos.objects.all()
    serializer = PlatosSerializer(platos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualizarPerfil(request):
    usuario = request.user
    serializer = UsuariosSerializer(instance=usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def lista_user(request):
    custom = Usuarios.objects.all()
    serializer = UsuariosSerializer(custom, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def eliminar_usuarios(request,pk):
    try:
        custom = Usuarios.objects.get(pk=pk)
    except Usuarios.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    custom.delete()
    return Response({'message': 'Usuario eliminado'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def filtrar_platos(request):
    platos_filter = PlatosFilter(request.GET, queryset=Platos.objects.all())
    serializer = PlatosSerializer(platos_filter.qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agregar_comentario(request, plato_id):
    serializer = ComentariosSerializer(data=request.data, context={'plato_id': plato_id, 'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ver_comentarios(request, plato_id):
    comentarios = Comentarios.objects.select_related('usuario', 'plato')  # Incluye usuario y plato
    serializer = ComentariosDetalleSerializer(comentarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def actualizar_Usuario(request, pk):
    try:
        custom = Usuarios.objects.get(pk=pk)
    except Usuarios.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsuariosSerializer(custom, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'custom': serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comentario_list(request, plato_id):
    try:
        plato = Platos.objects.get(id=plato_id)
    except Platos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comentarios = plato.comentarios.all()
        serializer = ComentariosDetalleSerializer(comentarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ComentariosDetalleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(plato=plato)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)