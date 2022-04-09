from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>/datosubasta", views.dato_subasta, name="datosubasta"),
    path("<int>user_id>/crear", views.crear, name="crear")
]
