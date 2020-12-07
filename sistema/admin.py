from django.contrib import admin
from .models import Morador, Visitante, Veiculo, AcessoInterno, AcessoExterno

# Register your models here.
admin.site.register(Morador)
admin.site.register(Visitante)
admin.site.register(Veiculo)
admin.site.register(AcessoInterno)
admin.site.register(AcessoExterno)