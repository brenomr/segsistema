from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('portaria/', portaria, name='portaria'),
    path('portaria/entrada/registrar/', registrar, name='registrar'),
    path('portaria/saida/', saida, name='saida'),
    path('busca/', busca, name='busca'),
    path('cadastro/', cadastro, name='cadastro'),
    path('cadastro/novo/<str:id>/', cadnovo, name='cadastro_novo'),
    path('cadastro/listar/', cadlistar, name='cadastro_listar'),
    path('cadastro/editar/<str:tabela>/<int:id>/', cadeditar, name='cadastro_editar'),
    path('consulta/', consultas, name='consulta'),
    path('consulta/acessos/', listar_consulta, name='listar_consulta'),
    path('ajuda/', ajuda, name='ajuda'),
    path('ajuda/perguntas/', perguntas, name='perguntas'),
    path('ajuda/manual/', manual, name='manual'),
    path('ajuda/sobre/', sobre, name='sobre'),
    path('logout/', deslogar, name='deslogar'),
    path('confirmar/', confirmacao, name='confirmacao'),
]