from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    foto_perfil = models.ImageField(upload_to='img/', null=True, blank=True)

class Platos(models.Model):
    foto_plato = models.ImageField(upload_to='img/', null=True, blank=True)
    nombre_plato = models.CharField(max_length=80)
    ingredientes = models.CharField(max_length=255)

    def __str__(self): 
        return self.nombre_plato

class Comentarios(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    plato = models.ForeignKey(Platos, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} sobre {self.plato.nombre_plato}"
