from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .form import AcessoVisitante, AcessoMorador, Filtro, MoradorForm, VisitanteForm, VeiculoForm, VeiculoVisitante, VeiculoMorador
from .models import AcessoExterno, AcessoInterno, Morador, Visitante, Veiculo
from django.db import Error
from django.db.models import Q
import datetime
from itertools import chain

verificar = '' # VAR GLOBAL p/ verificação do tipo de usuário

def relogio():
    data = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
    return (data)

def deslogar(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html', {'data' : relogio,'titulo':'Principal'})

@login_required
def portaria(request):
    return render(request, 'portaria.html', {'data' : relogio,'titulo':'Portaria'})

@login_required
def confirmacao(request,tipo,conf): # BLOCO DE CONFIRMAÇÕES E ERROS

    if tipo == 'erro':

        resultado = {
            1:'Utilize o menu Consultas > Cadastros e selecione o tipo de lista que pretende consultar',    # Ocorre se o usuário tentar acessar o cadastro/listar sem usar o menu
            2:'Nenhum formulário atende a requisição',                                                      # Ocorre se houver erro na variável global
            3:'O cartão está em uso ou o visitante informado está dentro do condomínio, verifique o acesso e tente novamente',
            4:'O cartão informado não está em uso',
            5:'O campo do cartão não pode ser vazio',
            6:'O tipo de cadastro solicitado não existe, favor utilizar uma das opções informadas no menu Cadastrar',
            7:'A tabela requisitada para pesquisa não existe, favor escolher entre morador, visitante ou veículo',
            8:'O item solicitado não existe, evite passar os dados pela barra de URL, utilize apenas os itens da lista',
            9:'Erro na consulta, formulário inválido, tente novamente',                                     # Ocorre em tentativa de injection
        }

        resultado = resultado.get(conf)
        return render(request,'confirmacao.html',{'data':relogio,'resultado':resultado,'classe':'fas fa-times fa-8x','cor':'Tomato','titulo':'Erro'})

    else:
        resultado = {
            1:'Registrado acesso do morador',
            2:'Registrado entrada do visitante',
            3:'Morador cadastrado com sucesso',
            4:'Cadastro atualizado',
            5:'Veículo de morador cadastrado com sucesso',
            6:'Veículo de visitante cadastrado com sucesso',
            7: 'Visitante cadastrado com sucesso',
        }

        resultado = resultado.get(conf)
        return render(request,'confirmacao.html',{'data':relogio,'resultado':resultado,'classe':'fas fa-check fa-8x','cor':'#00b33c','titulo':'Confirmação'})

@login_required
def registrar(request): # REGISTRAR ENTRADA (MORADOR/VISITANTE)
    try:  # TRY trata erro de exception caso o usuário tente registrar o mesmo cartão/visitante mais de uma vez (UNIQUE_TOGETHER)

        if request.method == 'POST':
            form = Filtro(request.POST) # RETORNA FORMULARIO P/ PREENCHIMENTO

            global verificar

            if form.is_valid():
                verificar = form.cleaned_data['item']

                if verificar == '1':
                    form = AcessoMorador()
                    titulo = 'Registrar Morador'
                else:
                    form = AcessoVisitante()
                    titulo = 'Registrar Visitante'

                return render(request, 'entrada.html', {'data': relogio, 'form': form, 'titulo': titulo})

            else:
                if verificar == '1':
                    form = AcessoMorador(request.POST or None)
                    resultado = 1
                else:
                    form = AcessoVisitante(request.POST or None)
                    resultado = 2

                if form.is_valid():
                    form.save()
                    return confirmacao(request,'ok',resultado)
                else:
                    return confirmacao(request,'erro',2)

        else:
            return confirmacao(request,'erro',1)

    except Error as e:
        return confirmacao(request,'erro',3)

@login_required
def saida(request): # REGISTRAR SAÍDA (VISITANTE)

    if request.method == 'POST':
        form = Filtro(request.POST)

        if form.is_valid():
            procura = form.cleaned_data['item']
            localizados = AcessoExterno.objects.filter(Q(cartao__icontains=procura) & Q(livre__icontains='nao'))

            if localizados.exists():
                for procura in localizados:
                    procura.saida = datetime.datetime.now()
                    procura.livre = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    procura.save()

                return render(request, 'confirmacao.html',
                              {'data':relogio,'resultado':'Foi registrado a saída de ' + procura.visitante.nome,
                               'classe':'fas fa-check fa-8x','cor':'#00b33c','titulo':'Confirmação'})

            else:
                return confirmacao(request,'erro',4)

        else:
            return confirmacao(request,'erro',5)

    else:
        return confirmacao(request, 'erro', 1)

@login_required
def cadastro(request):
    return render(request, 'cadastro.html', {'data' : relogio,'titulo':'Cadastro Geral'})

@login_required
def cadnovo(request,id): # INSERIR ITENS (MORADOR/VISITANTE/VEICULO)

    if id == 'morador':
        form = MoradorForm(request.POST or None)
        titulo = 'Cadastrar Morador'
        cad = 3

    elif id == 'visitante':
        form = VisitanteForm(request.POST or None)
        titulo = 'Cadastrar Visitante'
        cad = 7

    elif id == 'vmorador':
        form = VeiculoMorador(request.POST or None)
        titulo = 'Cadastrar Veículo Morador'
        cad = 5

    elif id == 'vvisitante':
        form = VeiculoVisitante(request.POST or None)
        titulo = 'Cadastrar Veículo Visitante'
        cad = 6

    else:
        return confirmacao(request,'erro',6)

    if form.is_valid():
        form.save()
        return confirmacao(request,'ok',cad)
    return render(request,'cadnovo.html',{'data':relogio,'form':form,'titulo':titulo})

@login_required
def cadlistar(request): # 'tabela' NECESSÁRIA P/ IDENTIFICAR A TABELA DO BD P/ EDIÇÃO DO ITEM

    if request.method=='POST':
        form = Filtro(request.POST)

        if form.is_valid():
            id = form.cleaned_data['item']

            if id == 'morador':
                lista = Morador.objects.all().order_by('nome')
                titulo = 'Lista de Moradores'
                tabela = 'morador'
            elif id == 'visitante':
                lista = Visitante.objects.all().order_by('nome')
                titulo = 'Lista de Visitantes'
                tabela = 'visitante'
            elif id == 'veiculo':
                lista = Veiculo.objects.all().order_by('placa')
                titulo = 'Lista de Veículos'
                tabela = 'veiculo'
            else:
                return confirmacao(request,'erro',7)

            return render(request, 'cadlistar.html', {'data' : relogio,'lista':lista,'titulo':titulo,'tabela':tabela})
        else:
            return confirmacao(request,'erro',2)
    else:
        return confirmacao(request,'erro',1)

@login_required
def cadeditar(request,tabela,id): # EDITAR/ATUALIZAR ITENS DO BD - (usa cadnovo como template, MUDAR ISSO PARA ADD EXCLUSÃO)

    if tabela == 'morador':
        localizado = get_object_or_404(Morador, pk=id)
        form = MoradorForm(request.POST or None, instance=localizado)
        titulo = 'Editar Morador'

    elif tabela == 'visitante':
        localizado = get_object_or_404(Visitante, pk=id)
        form = VisitanteForm(request.POST or None, instance=localizado)
        titulo = 'Editar Visitante'

    elif tabela =='veiculo':
        localizado = get_object_or_404(Veiculo, pk=id)
        form = VeiculoForm(request.POST or None, instance=localizado)
        titulo = 'Editar Veículo'

    else:
        return confirmacao(request,'erro',8)

    if form.is_valid():
        form.save()
        return confirmacao(request,'ok',4)
    return render(request,'cadnovo.html',{'data':relogio,'form':form,'titulo':titulo})

@login_required
def consultas(request):
    return render(request, 'consultas.html', {'data' : relogio,'titulo':'Consultar Acessos'})

@login_required
def listar_consulta(request): # LISTAR RELATÓRIO
    form = Filtro(request.POST)

    if form.is_valid():
        verificar = form.cleaned_data['item']

        if verificar == '1':
            lista = AcessoInterno.objects.all().order_by('-data')
            titulo = 'Acesso de Moradores'
            return render(request, 'consultainterna.html', {'data': relogio, 'lista': lista, 'titulo': titulo})

        else:
            lista = AcessoExterno.objects.all().order_by('-entrada')
            titulo = 'Acesso de Visitantes'
            return render(request, 'consultaexterna.html', {'data': relogio, 'lista': lista, 'titulo': titulo})

    else:
        return confirmacao(request,'erro',9)

@login_required
def busca(request):
    form = Filtro(request.POST) # ITEM BUSCADO

    if form.is_valid():
        busca = form.cleaned_data['item']
        morador = Morador.objects.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca))
        visitante = Visitante.objects.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca))
        veiculo = Veiculo.objects.filter(Q(modelo__icontains=busca) | Q(placa__icontains=busca))

        encontrados = chain(morador,visitante,veiculo)

        return render(request, 'busca.html',{'data': relogio,'encontrados':encontrados,'titulo':'Resultados'})

    else:
        return render(request, 'confirmacao.html',{'data': relogio, 'resultado': 'Erro no Form!', 'classe': 'fas fa-times fa-8x', 'cor': 'Tomato', 'titulo': 'Erro'})

def ajuda(request):
    return render(request, 'ajuda.html',{'data' : relogio,'titulo':'Ajuda'})

def perguntas(request):
    return render(request, 'perguntas.html', {'data' : relogio,'titulo':'Perguntas Frequentes'})

def manual(request):
    return render(request, 'manual.html', {'data' : relogio,'titulo':'Manual'})

def sobre(request):
    return render(request, 'sobre.html', {'data' : relogio,'titulo':'Sobre'})