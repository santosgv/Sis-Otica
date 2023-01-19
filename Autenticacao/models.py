from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from Unidades.models import UNIDADE


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
    UNIDADE = models.ForeignKey(UNIDADE,on_delete=models.DO_NOTHING,blank=True, null=True)

    def __str__(self) -> str:
        return str(self.username)


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.id


class SALARIO(models.Model):
    COLABORADOR = models.ForeignKey(USUARIO,on_delete=models.DO_NOTHING)
    VALOR = models.FloatField()
    DISCRIMINAÇAO = models.CharField(max_length=200,blank=True, null=True)
    DATA = models.DateTimeField()

    def __str__(self):
        return self.user.username

class COMISSAO(models.Model):
    VENDEDOR = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    VALOR =  models.FloatField(blank=True, null=True)
    VENDAS = models.IntegerField(blank=True, null=True)
    TICKET = models.FloatField(blank=True, null=True)
    COMISSAO = models.DecimalField(max_digits=2,decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.username


