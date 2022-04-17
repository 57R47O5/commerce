from asyncio.windows_events import NULL
from pickle import TRUE
from tkinter import CASCADE
from tokenize import blank_re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, ImageField, IntegerField


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=TRUE)    
    email = models.EmailField(blank=TRUE)
    password = models.CharField(max_length=64)    

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=64)

class Subasta(models.Model):
    creador_subasta = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Venta", null=TRUE)
    nombre_producto = models.CharField(max_length=64, null=TRUE)  
    categoria_producto = models.ForeignKey(Categoria, blank=TRUE, on_delete=models.CASCADE, null=TRUE, related_name="Producto")  
    imagen_producto = models.ImageField(blank = TRUE, null=TRUE)
    descripcion_producto = models.CharField(max_length=1024, null=TRUE)    
    precio_inicial = models.IntegerField(max_length=12, null=TRUE)
    ultimo_oferente =  models.ForeignKey(User, on_delete=models.SET_NULL, null=TRUE)
    estatus = models.BooleanField()

    def __str__(self) -> str:
        return self.nombre_producto 
        
class Oferta(models.Model):
    oferente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Oferta")  
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="Oferta")  
    precio = models.IntegerField(null= TRUE, editable=TRUE)

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comentario")  
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="Comentarios")  
    comentario = models.CharField(max_length=1024, editable=TRUE)

class Watchlist(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watchlist")
    subasta = models.ManyToManyField(Subasta, related_name = "SubastaWatchlist")