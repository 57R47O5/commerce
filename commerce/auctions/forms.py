from cProfile import label
from pickle import TRUE
from pyexpat import model
from django import forms
from django.forms import HiddenInput, ModelForm

from . models import Subasta

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
        fields = ['creador_subasta', 'nombre_producto', 'categoria_producto', 'imagen_producto', 'descripcion_producto', 'precio_inicial']
        widgets = {
            'creador_subasta': HiddenInput,  
            'descripcion_producto': forms.Textarea,          
        }

