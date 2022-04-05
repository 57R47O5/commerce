from pickle import TRUE
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, ImageField, IntegerField


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=TRUE)
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    email = models.EmailField(blank=TRUE)
    password = models.CharField(max_length=64)
    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=64)

class Producto(models.Model):        
    nombre_producto = models.CharField(max_length=64)  
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="Producto")  
    imagen_producto = models.ImageField(blank = TRUE)
    descripcion_producto = models.CharField(max_length=1024)

class Subasta(models.Model):
    creador_subasta = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Venta")
    producto_ofrecido = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="Subasta")
    precio_inicial = models.IntegerField
    
class Oferta(models.Model):
    oferente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Oferta")  
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="Oferta")  
    precio = models.IntegerField

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comentario")  
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="Comentarios")  
    comentario = CharField(max_length=1024)