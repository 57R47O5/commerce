from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Categoria)
admin.site.register(Subasta)
admin.site.register(Watchlist)
admin.site.register(Oferta)
admin.site.register(Comentario)
