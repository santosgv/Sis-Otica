from django.db import models
from django.contrib.auth.models import AbstractUser
from Unidades.models import UNIDADE


class Usuario(AbstractUser):

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

    NOME = models.CharField(max_length=100,blank=True, null=True)
    CPF = models.CharField(blank=True, max_length=18)
    DATA_NASCIMENTO = models.TimeField(blank=True, null=True)
    STATUS = models.CharField(max_length=1, choices=CHOICES_SITUACAO, default="A")
    FUNCAO = models.CharField(max_length=1, choices=CHOICES_FUNCAO)
    UNIDADE = models.ForeignKey(UNIDADE,on_delete=models.DO_NOTHING,blank=True, null=True)

    def __str__(self) -> str:
        return str(self.NOME)


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

