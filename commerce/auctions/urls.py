from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cerradas", views.cerradas, name="cerradas"),
    path("categorias", views.categorias, name="categorias"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>/datosubasta", views.dato_subasta, name="datosubasta"),
    path("<int:user_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:user_id>/agregar_watchlist", views.agregar_watchlist, name="agregar_watchlist"),
    path("<int:user_id>/eliminar_watchlist", views.eliminar_watchlist, name="eliminar_watchlist"),
    path("<int:subasta_id>/ver_subasta", views.ver_subasta, name="ver_subasta"),
    path("<int:subasta_id>/pujar", views.pujar, name="pujar"),
    path("<int:subasta_id>/comentar", views.comentar, name="comentar"),    
    path("<int:subasta_id>/cerrar", views.cerrar, name="cerrar"),
    path("<int:categoria_id>/categoria", views.categoria, name="categoria")    
]
