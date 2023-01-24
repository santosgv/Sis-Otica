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

    FILIAL= models.ForeignKey(UNIDADE, on_delete=models.DO_NOTHING)
    VENDEDOR = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    CLIENTE = models.ForeignKey(CLIENTE,on_delete=models.DO_NOTHING)
    DATA = models.DateTimeField(default=now)
    LENTES = models.CharField(max_length=500)
    RECEITA = models.TextField(max_length=2000)
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

class SERVICO(models.Model):
    NOME = models.CharField(max_length=500)

    def __str__(self):
        return str(self.NOME)

class SUB_SERVICO(models.Model):
    SERVICO = models.ForeignKey(SERVICO,on_delete=models.CASCADE)
    NOME = models.CharField(max_length=500)

    def __str__(self):
        return str(self.NOME)
        