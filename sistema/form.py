from django.forms import ModelForm
from django import forms
from .models import AcessoInterno, AcessoExterno, Morador, Visitante, Veiculo

class MoradorForm(ModelForm):
    class Meta:
        model = Morador
        fields = ['nome','cpf','endereco','observacao','telefone','celular']
        widgets = {'nome':forms.TextInput(attrs={'placeholder':'Digite seu nome'}),
                   'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
                   'endereco': forms.TextInput(attrs={'placeholder': 'Digite seu endereço'}),
                   'telefone': forms.TextInput(attrs={'placeholder': '(00) 0000-0000'}),
                   'celular': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
                   }

class VisitanteForm(ModelForm):
    class Meta:
        model = Visitante
        fields = ['nome','cpf','observacao','telefone','celular']
        widgets = {'nome': forms.TextInput(attrs={'placeholder': 'Digite seu nome'}),
                   'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
                   'telefone': forms.TextInput(attrs={'placeholder': '(00) 0000-0000'}),
                   'celular': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
                   }

class VeiculoForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','modelo','cor','observacao','morador','visitante']
        widgets = {'placa': forms.TextInput(attrs={'placeholder': 'AAA 1234'}),
                   'modelo': forms.TextInput(attrs={'placeholder': 'Digite o modelo do veículo'}),
                   }

class VeiculoMorador(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','modelo','cor','observacao','morador']
        widgets = {'placa': forms.TextInput(attrs={'placeholder': 'AAA 1234','style': 'text-transform:uppercase;'}),
                   'modelo': forms.TextInput(attrs={'placeholder': 'Digite o modelo do veículo'}),
                   'cor': forms.TextInput(attrs={'placeholder': 'Digite a cor do veículo'}),
                   }

    def clean_placa(self):
        return self.cleaned_data['placa'].upper()

class VeiculoVisitante(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','modelo','cor','observacao','visitante']
        widgets = {'placa': forms.TextInput(attrs={'placeholder': 'AAA 1234','style': 'text-transform:uppercase;'}),
                   'modelo': forms.TextInput(attrs={'placeholder': 'Digite o modelo do veículo'}),
                   'cor': forms.TextInput(attrs={'placeholder': 'Digite a cor do veículo'}),
                   }

    def clean_placa(self):
        return self.cleaned_data['placa'].upper()

class AcessoMorador(ModelForm):
    def __init__(self,*args,**kwargs): # Torna campo READONLY para evitar edição
        super(AcessoMorador, self).__init__(*args,**kwargs)
        self.fields['data'].widget.attrs['readonly'] = True

    class Meta:
        model = AcessoInterno
        fields = ['tipo', 'data', 'morador', 'veiculo']
        labels = {
            'tipo': 'Tipo*',
            'morador': 'Morador*',
            'veiculo': 'Veículo',

        }

class AcessoVisitante(ModelForm):
    def __init__(self,*args,**kwargs):
        super(AcessoVisitante, self).__init__(*args,**kwargs)
        self.fields['entrada'].widget.attrs['readonly'] = True

    class Meta:
        model = AcessoExterno
        fields = ['cartao','entrada', 'visitante', 'veiculo']
        labels = {'cartao':'Cartão*','visitante':'Visitante*','veiculo':'Veículo'}
        widgets = {'cartao': forms.TextInput(attrs={'placeholder': 'Digite o número do cartão'}),
                   }

class Filtro(forms.Form):
    item = forms.CharField()