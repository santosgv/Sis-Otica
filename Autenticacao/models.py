from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from Unidades.models import UNIDADE,CLIENTE,PERTO,LONGE


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

    NOME = models.CharField(max_length=100,blank=True, null=True)
    CPF = models.CharField(blank=True, max_length=18)
    DATA_NASCIMENTO = models.DateField(blank=True, null=True)
    STATUS = models.CharField(max_length=1, choices=CHOICES_SITUACAO, default="A")
    FUNCAO = models.CharField(max_length=1, choices=CHOICES_FUNCAO,blank=True, null=True)
    UNIDADE = models.ForeignKey(UNIDADE,on_delete=models.DO_NOTHING,blank=True, null=True)

    def __str__(self) -> str:
        return str(self.NOME)


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


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


class ORDEN(models.Model):

    CHOICES_SITUACAO =(
        ('A','EM ABERTO'),
        ('E','ENCERRADO'),
        ('C','CANCELADO'),
    )

    CHOICES_PAGAMENTO =(
        ('D','DINHEIRO'),
        ('C','CARTAO'),
        ('A','CARNER'),
    )

    FILIAL= models.ForeignKey(UNIDADE, on_delete=models.DO_NOTHING)
    VENDEDOR = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    CLIENTE = models.ForeignKey(CLIENTE,on_delete=models.DO_NOTHING)
    DATA = models.DateTimeField(default=datetime.datetime.now())
    LENTES = models.CharField(max_length=500)
    LONGE = models.ForeignKey(LONGE, on_delete=models.DO_NOTHING)
    PERTO = models.ForeignKey(PERTO, on_delete=models.DO_NOTHING)
    ARMACAO = models.CharField(max_length=500)
    TRATAMENTO = models.CharField(max_length=500)
    OBSERVACAO = models.TextField(max_length=1000)
    VALOR = models.FloatField()
    FORMA_PAG = models.CharField(max_length=1, choices=CHOICES_PAGAMENTO)
    ENTRADA = models.FloatField()
    PREVISAO_ENTREGA = models.DateField()
    QUANTIDADE_PARCELA = models.IntegerField()
    ANEXO =  models.ImageField(upload_to='anexo_img' ,blank=True, null=True)
    STATUS = models.CharField(max_length=1 , choices=CHOICES_SITUACAO, default='A')

    def __str__(self):
        return str(self.id)