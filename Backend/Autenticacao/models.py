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

    def __str__(self) -> str:
        return str(self.username)


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Colaborador(models.Model):
    usuario = models.OneToOneField(USUARIO, on_delete=models.CASCADE)
    salario_bruto = models.FloatField()
    comissao_percentual = models.FloatField(default=0.0)  # Percentual de comissão
    data_contratacao = models.DateField()

    def __str__(self):
        return self.usuario.first_name
    

    
class Desconto(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    percentual = models.FloatField()  

    def __str__(self):
        return f"{self.tipo} - {self.colaborador.usuario.first_name}"

class Comissao(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    valor_vendas = models.FloatField() 
    data_referencia = models.DateField()  

    def calcular_comissao(self):
        return self.valor_vendas * (self.colaborador.comissao_percentual / 100)

    def __str__(self):
        return f"Comissão - {self.colaborador.usuario.username} - {self.data_referencia}"