from cProfile import label
from pickle import TRUE
from pyexpat import model
from django import forms
from django.forms import HiddenInput, IntegerField, ModelForm

from . models import Oferta, Subasta, Comentario

# En este archivo definimos los formularios a ser utilizados en view

# Fromulario para crear subasta

class crear_subasta_form(forms.Form):
    creador_subasta = forms.CharField(label="Usuario", required=TRUE, widget=HiddenInput)
    nombre_producto = forms.CharField(label="nombre_producto", required=True)
    categoria_producto = forms.ChoiceField(label="Categoria", required=False)
    imagen_producto = forms.URLField(label="Imagen", required=False)
    descripcion_producto = forms.CharField(label="Descripcion", required=TRUE ,widget=forms.Textarea)
    precio_inicial = forms.IntegerField(label="Precio", required=TRUE)    
    

class SubastaForm(ModelForm):    
    class Meta:
        model = Subasta
        fields = ['creador_subasta', 'nombre_producto', 'categoria_producto', 'imagen_producto', 'descripcion_producto', 'precio_inicial','estatus']
        widgets = {              
            'ultimo_oferente': HiddenInput,
            'descripcion_producto': forms.Textarea,   
            'estatus': HiddenInput,
        }

class OfertaForm(ModelForm):
    class Meta:
        model = Oferta
        fields = ['oferente','subasta','precio']
        widgets = {
            'oferente': HiddenInput,
            'subasta': HiddenInput,              
        }

class WatchlistForm(forms.Form):
    id_producto = forms.IntegerField(label="Producto", required=TRUE, widget=HiddenInput)

class UserForm(forms.Form):
    id_usuario = forms.IntegerField(required=TRUE)

class ComentarioForm(forms.Form):
    class Meta:
        model = Comentario
        fields = ['usuario', 'subasta', 'comentario']
        widgets = {
            'usuario': HiddenInput,
            "subasta": HiddenInput,
            'comentario': forms.Textarea
        }

