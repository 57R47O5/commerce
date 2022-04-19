from pickle import FALSE
import re
from tkinter import EW
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from django.forms import formset_factory

# Funciones

def index(request):    
    Subastas = Subasta.objects.filter(estatus=True)                             # Subastas abiertas
    contexto = {"subastas":Subastas}                                            # Añadimos al contexto    
    form1 = WatchlistForm()
    contexto.update({"form1":form1})
    return render(request, "auctions/index.html", contexto)

def cerradas(request):    
    Subastas = Subasta.objects.filter(estatus=False)                             # Subastas abiertas
    contexto = {"subastas":Subastas}                                            # Añadimos al contexto        
    return render(request, "auctions/cerradas.html", contexto)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categorias(request):
    categorias = Categoria.objects.all()    
    contexto = {"categorias":categorias}
    return render(request, "auctions/categorias.html", contexto)

# Recibimos los datos que nos envía el form, y el id del usuario, creamos una nueva subasta y nos dirigimos a su página
def dato_subasta(request, user_id):
    contexto = {"usuario_id":user_id, "view":"dato_subasta"}
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        subasta = SubastaForm(request.POST, request.FILES)    # Aparentemente llega la imagen, pero no guarda    
        if subasta.is_valid():                     
            tabla_subasta = subasta.cleaned_data
            subasta.save()                
            subasta.ultimo_oferente = user  
            subasta.save()                        
            contexto.update(tabla_subasta)
            contexto.update({"subastas":Subasta.objects.all()})
            return index(request)
        else:
            return render(request, "auctions/error.html", contexto)
    else:
        subasta = SubastaForm(initial={'creador_subasta':user_id, 'estatus':TRUE })                        
        contexto.update({"subasta": subasta})
        return render(request, "auctions/subasta.html", contexto)

@login_required
def watchlist(request, user_id):
    #watchlists = Watchlist.objects.filter(usuario=user_id)      # Objeto queryset. Tenemos que sacar de aca un list de elementos subasta
    #watchlists.save()    
    subastas = Subasta.objects.filter(SubastaWatchlist__usuario=user_id)    
    contexto=({"subastas":subastas})
    return render(request, "auctions/watchlist.html", contexto)

@login_required
def agregar_watchlist(request, user_id):
    if request.method == "POST":
        producto =  WatchlistForm(request.POST)
        if producto.is_valid():
            tabla_producto = producto.cleaned_data                            
            usuario = User.objects.get(pk=user_id)    # Objeto User 
            subasta = Subasta.objects.get(pk=tabla_producto["id_producto"])     # Objeto Subasta
            w = Watchlist(usuario=usuario)                     
            w.save()
            w.subasta.add(subasta)
    return index(request)

@login_required
def eliminar_watchlist(request, user_id):
    if request.method == "POST":
        producto =  WatchlistForm(request.POST)
        if producto.is_valid():
            tabla_producto = producto.cleaned_data   
            usuario = User.objects.get(pk=user_id)
            subasta = Subasta.objects.get(pk=tabla_producto["id_producto"])                 
            w = Watchlist.objects.get(usuario=user_id, subasta=subasta)         
            w.delete()
    return index(request)

def ver_subasta(request, subasta_id):
    subasta = Subasta.objects.get(pk=subasta_id)    # Buscamos la subasta
    creador = subasta.creador_subasta            # Tenemos al creador
    id_usuario = request.user.pk                    # Usuario actual 
    contexto = {"subasta":subasta, "id_usuario":id_usuario, "creador":creador}        
    s = Watchlist.objects.filter(usuario = id_usuario, subasta=subasta_id)
    c = s.count()                                  
    contexto.update({"c":c})
    opiniones = Comentario.objects.filter(subasta=subasta_id)    
    a = opiniones.count()                                  
    contexto.update({"a":a, "opiniones":opiniones})
    comentario = ComentarioForm(initial={"usuario":id_usuario, "subasta":subasta_id})
    contexto.update({"comentario":comentario})
    return render(request, "auctions/ver_subasta.html", contexto)   


@login_required
def pujar(request, subasta_id):
    subasta = Subasta.objects.get(pk=subasta_id)                                              
    contexto = {"subasta":subasta}
    contexto.update({"view":"pujar"})    
    if request.method == "POST":
        oferta = OfertaForm(request.POST)
        if oferta.is_valid():
            datos = oferta.cleaned_data            # Tiene el formato del modelo Oferta (oferente, subasta, precio)
            PrecioOferta = datos["precio"]
            Oferente = datos["oferente"]
            subasta = Subasta.objects.get(pk=subasta_id)
            if Oferente != subasta.creador_subasta:
                if PrecioOferta > subasta.precio_inicial:
                    subasta.precio_inicial = PrecioOferta
                    subasta.ultimo_oferente = Oferente
                    subasta.save()
                    return index(request)
                else:
                    return render(request, "auctions/errorpuja.html")
            else:                
                return render(request, "auctions/erroruser.html")                                                                 
        else:
            return render(request, "auctions/error.html", contexto)

@login_required
def cerrar(request, subasta_id):
    subasta = Subasta.objects.get(pk=subasta_id) 
    subasta.estatus = False  
    subasta.save()                                           
    contexto = {"subasta":subasta}    
    return render(request, "auctions/ver_subasta.html",contexto)

@login_required
def comentar(request, subasta_id):
    user_id = request.user.pk
    if request.method == "POST":
        comentario = ComentarioForm(request.POST)
        if comentario.is_valid:
            comentario.save()            
            return index(request)            
    else:
        comentario = ComentarioForm(initial={"usuario":user_id})
    return index(request)

def categoria(request, categoria_id):
    subastas = Subasta.objects.filter(categoria_producto_id=categoria_id)
    bandera = subastas.count()
    contexto = {"subastas":subastas, "bandera":bandera}
    return render(request, "auctions/categoria.html", contexto)