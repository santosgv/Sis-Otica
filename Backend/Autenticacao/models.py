from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now



class USUARIO(AbstractUser):

    CHOICES_SITUACAO =(
        ('A','Ativo'),
        ('F','Ferias'),
        ('I','Inativo'),
    )

    CHOICES_FUNCAO =(
        ('V','Vendedor'),
        ('C','Caixa'),
        ('G','Gerente'),
    )

    CPF = models.CharField(blank=True, max_length=18)
    DATA_NASCIMENTO = models.DateField(blank=True, null=True)
    STATUS = models.CharField(max_length=1, choices=CHOICES_SITUACAO, default="A")
    FUNCAO = models.CharField(max_length=1, choices=CHOICES_FUNCAO,blank=True, null=True)
    salario_bruto = models.FloatField(default=0.0)
    comissao_percentual = models.FloatField(default=0.0)
    valor_hora = models.FloatField(default=0.0)
    data_contratacao = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.first_name)


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
    
    
class Desconto(models.Model):
    colaborador = models.ForeignKey(USUARIO, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    percentual = models.FloatField()  

    def __str__(self):
        return f"{self.tipo} - {self.colaborador.first_name}"

class Comissao(models.Model):
    colaborador = models.ForeignKey(USUARIO, on_delete=models.CASCADE)
    valor_vendas = models.FloatField() 
    data_referencia = models.DateField()  
    horas_extras = models.FloatField(default=0.0)

    def calcular_comissao(self):
        return self.valor_vendas * (self.colaborador.comissao_percentual / 100)

    def calcula_horas_extras(self):
        return self.horas_extras * (self.colaborador.valor_hora * 1.50 )

    def __str__(self):
        return f"Comissão - {self.colaborador.username} - {self.data_referencia}"