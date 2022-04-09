from asyncio.windows_events import NULL
from pickle import TRUE
from tkinter import CASCADE
from tokenize import blank_re
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

class Subasta(models.Model):
    creador_subasta = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Venta", null=TRUE)
    nombre_producto = models.CharField(max_length=64, null=TRUE)  
    categoria_producto = models.ForeignKey(Categoria, blank=TRUE, on_delete=models.CASCADE, null=TRUE, related_name="Producto")  
    imagen_producto = models.ImageField(blank = TRUE, null=TRUE)
    descripcion_producto = models.CharField(max_length=1024, null=TRUE)    
    precio_inicial = models.IntegerField(max_length=12, null=TRUE)

    def crear_vacio(self):
        creador_subasta = NULL
        nombre_producto = NULL
        categoria_producto = NULL
        imagen_producto = NULL
        descripcion_producto = NULL
        precio_inicial = NULL
        Subasta.save()

    
class Oferta(models.Model):
    oferente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Oferta")  
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="Oferta")  
    precio = models.IntegerField

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comentario")  
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="Comentarios")  
    comentario = CharField(max_length=1024)