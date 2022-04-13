from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>/datosubasta", views.dato_subasta, name="datosubasta"),
    path("<int:user_id>/agregar_watchlist", views.agregar_watchlist, name="agregar_watchlist"),
    path("<int:user_id>/eliminar_watchlist", views.eliminar_watchlist, name="eliminar_watchlist"),
    path("<int:subasta_id>/ver_subasta", views.ver_subasta, name="ver_subasta"),
    path("<int:subasta_id>/pujar", views.pujar, name="pujar"),
    path("<int:user_id>/crear", views.crear, name="crear")
]
