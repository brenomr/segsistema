from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Morador(models.Model):
    nome = models.CharField(max_length=30,unique=True,verbose_name="Nome*")
    cpf = models.CharField(max_length=14, unique=True,verbose_name="CPF*")
    endereco = models.CharField(max_length=30,verbose_name="Endereço*")
    observacao = models.TextField(null=True,blank=True,verbose_name="Observação")
    telefone = models.CharField(max_length=14,null=True,blank=True,verbose_name="Telefone")
    celular = models.CharField(max_length=15,null=True,blank=True,verbose_name="Celular")

    class Meta:
        verbose_name_plural = 'Morador'

    def __str__(self):
        return self.nome

class Visitante(models.Model):
    nome = models.CharField(max_length=30,unique=True,verbose_name="Nome*")
    cpf = models.CharField(max_length=14, unique=True,verbose_name="CPF*")
    observacao = models.TextField(null=True,blank=True,verbose_name="Observação")
    telefone = models.CharField(max_length=14,null=True,blank=True,verbose_name="Telefone")
    celular = models.CharField(max_length=15, null=True,blank=True,verbose_name="Celular")

    class Meta:
        verbose_name_plural = 'Visitante'

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    modelo = models.CharField(max_length=20,verbose_name="Modelo*")
    placa = models.CharField(max_length=8,unique=True,verbose_name="Placa*")
    cor = models.CharField(max_length=10,verbose_name="Cor*")
    observacao = models.TextField(null=True,blank=True,verbose_name="Observação")
    morador = models.ForeignKey(Morador,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Morador*")
    visitante = models.ForeignKey(Visitante,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Visitante*")

    class Meta:
        verbose_name_plural = 'Veiculo'

    def clean(self):
        super().clean()
        if self.morador is None and self.visitante is None:
            raise ValidationError('O veículo precisa de pelo menos um proprietário')

    def __str__(self):
        return self.placa

class AcessoInterno(models.Model):
    entrada = 'Entrada'
    saida = 'Saída'
    tipos = [(entrada,'Entrada'),(saida,'Saída'),]
    tipo = models.CharField(max_length=7,choices=tipos,default=entrada,)
    data = models.DateTimeField(default=now)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, null=True, blank=True)
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE,  null=False)

    class Meta:
        verbose_name_plural = 'Acesso Interno'

    def __str__(self):
        return self.morador.nome

class AcessoExterno(models.Model):
    cartao = models.CharField(max_length=10)
    entrada = models.DateTimeField(default=now)
    saida = models.DateTimeField(null=True, blank=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, null=True, blank=True)
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, null=False)
    livre = models.CharField(max_length=20, default='nao')

    class Meta:
        verbose_name_plural = 'Acesso Externo'
        unique_together = (('cartao', 'livre',), ('visitante', 'livre'))

    def __str__(self):
        return self.cartao