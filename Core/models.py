from django.db import models
from Autenticacao.models import USUARIO
from Unidades.models import UNIDADE
from django.utils.timezone import now






class CLIENTE(models.Model):
    NOME = models.CharField(max_length=250)
    LOGRADOURO = models.CharField(max_length=250)
    NUMERO = models.CharField(max_length=10)
    BAIRRO = models.CharField(max_length=200)
    CIDADE = models.CharField(max_length=200)
    TELEFONE = models.CharField(max_length=30, blank=True, null=True)
    CPF = models.CharField(max_length=14)
    DATA_NASCIMENTO = models.DateField(blank=True, null=True)
    EMAIL = models.CharField(max_length=100,blank=True, null=True)
    FOTO =  models.ImageField(upload_to='foto_img',blank=True, null=True)
    DATA_CADASTRO = models.DateField(default=now)

    def __str__(self) -> str:
        return str(self.NOME)

class ORDEN(models.Model):

    CHOICES_SITUACAO =(
        ('A','EM ABERTO'),
        ('E','ENCERRADO'),
        ('C','CANCELADO'),
    )

    CHOICES_PAGAMENTO =(
        ('A','PIX'),
        ('B','DINHEIRO'),
        ('C','DEBITO'),
        ('D','CREDITO'),
        ('E','CARNER'),
        ('F','PERMUTA'),
    )

    STATUS = models.CharField(max_length=1 , choices=CHOICES_SITUACAO, default='A')
    ANEXO =  models.ImageField(upload_to='anexo_img' ,blank=True, null=True)
    FILIAL= models.ForeignKey(UNIDADE, on_delete=models.DO_NOTHING)
    VENDEDOR = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    CLIENTE = models.ForeignKey(CLIENTE,on_delete=models.DO_NOTHING)
    DATA = models.DateTimeField(default=now)
    PREVISAO_ENTREGA = models.DateField()
    SERVICO = models.CharField(max_length=500)
    SUB_SERVICO = models.CharField(max_length=500)
    RECEITA = models.TextField(max_length=2000)
    LENTES = models.CharField(max_length=500)
    ARMACAO = models.CharField(max_length=500)
    OBSERVACAO = models.TextField(max_length=1000)
    FORMA_PAG = models.CharField(max_length=1, choices=CHOICES_PAGAMENTO)
    VALOR = models.FloatField()
    QUANTIDADE_PARCELA = models.IntegerField()
    ENTRADA = models.FloatField()
    

    def __str__(self):
        return str(self.id)


