from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, ImageField, IntegerField


class User(AbstractUser):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):        
    nombre = models.CharField(max_length=64)    
    imagen = models.ImageField
    descripcion = models.CharField(max_length=1024)

class Subasta(models.Model):
    creador = models.ForeignKey(User, on_delete=CASCADE, related_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=CASCADE, related_name="Subasta")
    precio_inicial = models.IntegerField(max_length=8)
    
class Oferta(models.Model):
    oferente = models.ForeignKey(User, on_delete=CASCADE, related_name="Oferta")  
    subasta = models.ForeignKey(Subasta, on_delete=CASCADE, related_name="Oferta")  
    precio = models.IntegerField(max_length=8)
    
class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=CASCADE, related_name="Comentario")  
    subasta = models.ForeignKey(Subasta, on_delete=CASCADE, related_name="Comentarios")  
    comentario = CharField(max_length=1024)