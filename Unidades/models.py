from django.db import models
import datetime
from Autenticacao.models import USUARIO


class UNIDADE(models.Model):
    NOME = models.CharField(max_length=100)
    CNPJ = models.CharField(max_length=18)

    def __str__(self) -> str:
        return str(self.NOME)

class CUSTO(models.Model):

    CHOICES_FORMA =(
        ('S','SEMANAL'),
        ('M','MENSAL'),
        ('Q','QUINZENAL'),
    )

    CONTA = models.CharField(max_length=100, blank=True)
    FILIAL = models.ForeignKey(UNIDADE, on_delete=models.DO_NOTHING)
    VALOR = models.FloatField()
    VENCIMENTO = models.DateTimeField()
    FORMA = models.CharField(max_length=1, choices=CHOICES_FORMA, default="M")
    PERIODO =models.IntegerField()

class SALARIO(models.Model):
    COLABORADOR = models.ForeignKey(USUARIO,on_delete=models.DO_NOTHING)
    VALOR = models.FloatField()
    DISCRIMINAÇAO = models.CharField(max_length=200,blank=True, null=True)
    DATA = models.DateTimeField()

class COMISSAO(models.Model):
    #VENDEDOR = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    VALOR =  models.FloatField(blank=True, null=True)
    VENDAS = models.IntegerField(blank=True, null=True)
    TICKET = models.FloatField(blank=True, null=True)
    COMISSAO = models.DecimalField(max_digits=2,decimal_places=2, blank=True, null=True)

class LONGE(models.Model):
    LONGE_OD_ESF = models.FloatField(blank= True, null=True)
    LONGE_OD_CIL = models.FloatField(blank= True, null=True)
    LONGE_OD_EIXO = models.FloatField(blank= True, null=True)
    LONGE_OD_DNP = models.FloatField(blank= True, null=True)
    LONGE_OD_AL = models.FloatField(blank= True, null=True)
    LONGE_OD_AD = models.FloatField(blank= True, null=True)
    LONGE_OE_ESF = models.FloatField(blank= True, null=True)
    LONGE_OE_CIL = models.FloatField(blank= True, null=True)
    LONGE_OE_EIXO = models.FloatField(blank= True, null=True)
    LONGE_OE_DNP = models.FloatField(blank= True, null=True)
    LONGE_OE_AL = models.FloatField(blank= True, null=True)
    LONGE_OE_AD = models.FloatField(blank= True, null=True)

class PERTO(models.Model):
    PERTO_OD_ESF = models.FloatField(blank= True, null=True)
    PERTO_OD_CIL = models.FloatField(blank= True, null=True)
    PERTO_OD_EIXO = models.FloatField(blank= True, null=True)
    PERTO_OD_DNP = models.FloatField(blank= True, null=True)
    PERTO_OD_AL = models.FloatField(blank= True, null=True)
    PERTO_OD_AD = models.FloatField(blank= True, null=True)
    PERTO_OE_ESF = models.FloatField(blank= True, null=True)
    PERTO_OE_CIL = models.FloatField(blank= True, null=True)
    PERTO_OE_EIXO = models.FloatField(blank= True, null=True)
    PERTO_OE_DNP = models.FloatField(blank= True, null=True)
    PERTO_OE_AL = models.FloatField(blank= True, null=True)
    PERTO_OE_AD = models.FloatField(blank= True, null=True)

class CLIENTE(models.Model):
    NOME = models.CharField(max_length=250)
    LOGRADOURO = models.CharField(max_length=250)
    NUMERO = models.CharField(max_length=10)
    BAIRRO = models.CharField(max_length=200)
    CIDADE = models.CharField(max_length=200)
    TELEFONE = models.CharField(max_length=30, blank=True, null=True)
    CPF = models.CharField(max_length=14)
    DATA_NASCIMENTO = models.DateTimeField(blank=True, null=True)
    EMAIL = models.CharField(max_length=100,blank=True, null=True)
    LONGE = models.ForeignKey(LONGE , on_delete=models.CASCADE, blank=True, null=True)
    PERTO = models.ForeignKey(PERTO, on_delete=models.CASCADE, blank=True, null=True)
    FOTO =  models.ImageField(upload_to='foto_img',blank=True, null=True)

class CLIENTE_EXAME(models.Model):
    CLIENTE = models.ForeignKey (CLIENTE,on_delete=models.CASCADE)
    LONGE = models.ForeignKey(LONGE , on_delete=models.CASCADE)
    PERTO = models.ForeignKey(PERTO, on_delete=models.CASCADE)
    
class ORDEM_SERVICO(models.Model):

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
    #VENDEDOR = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
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