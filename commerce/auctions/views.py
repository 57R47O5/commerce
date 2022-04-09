from tkinter import EW
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from django.forms import formset_factory

# Funciones

def index(request):
    return render(request, "auctions/index.html")


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

# Recibimos los datos que nos envía el form, y el id del usuario, creamos una nueva subasta y nos dirigimos a su página
def dato_subasta(request, user_id):
    contexto = {"usuario_id":user_id, "view":"dato_subasta"}
    if request.method == "POST":
        subasta = SubastaForm(request.POST)        
        if subasta.is_valid():                     
            tabla_subasta = subasta.cleaned_data
            datos = subasta.save()                             
            contexto.update(tabla_subasta)
            return render(request, "auctions/subasta.html", contexto)  
        else:
            return render(request, "auctions/error.html", contexto)
    else:
        subasta = SubastaForm(initial={'creador_subasta':user_id })                        
        contexto.update({"subasta": subasta})
        return render(request, "auctions/subasta.html", contexto)
 


def crear(request, user_id):
    if request.method == 'POST':
        subasta = forms.crear_subasta_form
        if subasta.is_valid():
            datos_subasta = subasta.cleaned_data
            context = datos_subasta
            return render(request, "auctions/subasta.html", context)
    else:
        return render(request, "auctions/error.html", context)