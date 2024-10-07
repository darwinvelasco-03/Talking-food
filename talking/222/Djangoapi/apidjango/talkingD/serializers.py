from rest_framework import serializers
from .models import *

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ('id' , 'foto_perfil', 'first_name', 'last_name', 'username','email','password','is_staff')
        extra_kwargs = {
            'is_staff': {'read_only': False}, 
        }
        

        def create(self, validated_data):
            user = Usuarios.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )
            if 'is_staff' in validated_data:
                user.is_staff = validated_data['is_staff']
                user.save()
            return user
        
class PlatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platos
        fields = ['id', 'foto_plato', 'nombre_plato', 'ingredientes']

class ComentariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comentarios
        fields = ['id', 'comentario', 'fecha', 'usuario_id', 'plato_id']  # Eliminar 'plato' y 'usuario'
        read_only_fields = ['fecha']  # 'fecha' es solo de lectura

    def create(self, validated_data):
        request = self.context.get('request')
        plato_id = self.context.get('plato_id')
        comentario = Comentarios.objects.create(
            plato_id=plato_id,
            usuario=request.user,
            **validated_data
        )
        return comentario

class ComentariosDetalleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='usuario.username', read_only=True)
    nombre_plato = serializers.CharField(source='plato.nombre_plato', read_only=True)

    class Meta:
        model = Comentarios
        fields = ['id', 'comentario', 'fecha', 'username', 'nombre_plato']
