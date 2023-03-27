from django.db import models
from Autenticacao.models import USUARIO
from Unidades.models import UNIDADE
from django.utils.timezone import now






class CLIENTE(models.Model):
    UNIDADE = models.ForeignKey(UNIDADE,on_delete=models.DO_NOTHING,blank=True, null=True)
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
        ('A','SOLICITADO'),
        ('E','ENTREGUE'),
        ('C','CANCELADO'),
        ('L','LABORATÓRIO'),
        ('J','LOJA')
    )

    CHOICES_PAGAMENTO =(
        ('A','PIX'),
        ('B','DINHEIRO'),
        ('C','DEBITO'),
        ('D','CREDITO'),
        ('E','CARNER'),
        ('F','PERMUTA'),
    )
    DATA_SOLICITACAO = models.DateField(default=now)
    STATUS = models.CharField(max_length=1 , choices=CHOICES_SITUACAO, default='A')
    ANEXO =  models.ImageField(upload_to='anexo_img' ,blank=True, null=True)
    FILIAL= models.ForeignKey(UNIDADE, on_delete=models.DO_NOTHING)
    VENDEDOR = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    CLIENTE = models.ForeignKey(CLIENTE,on_delete=models.DO_NOTHING)
    DATA = models.DateTimeField(default=now)
    PREVISAO_ENTREGA = models.DateField()
    ASSINATURA = models.ImageField(upload_to='assinatura_img' ,blank=True, null=True)
    SERVICO = models.CharField(max_length=500)
    SUB_SERVICO = models.CharField(max_length=500)
    OD_ESF = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OD_CIL = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OD_EIXO = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OE_ESF = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OE_CIL = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OE_EIXO = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    AD = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    DNP = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    P = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    DPA = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    DIAG = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    V = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    H = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    ALT = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    ARM = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    MONTAGEM = models.CharField(max_length=500,blank=True, null=True,default='N/D')
    LENTES = models.CharField(max_length=500,blank=True, null=True,default='N/D')
    ARMACAO = models.CharField(max_length=500, blank=True, null=True,default='N/D')
    OBSERVACAO = models.TextField(max_length=1000, blank=True, null=True,default='N/D')
    FORMA_PAG = models.CharField(max_length=1, choices=CHOICES_PAGAMENTO,blank=True, null=True,default='N/D')
    VALOR =  models.CharField(max_length=100,default='N/D')
    QUANTIDADE_PARCELA = models.IntegerField(blank=True, null=True,default='N/D')
    ENTRADA = models.CharField(max_length=100)
    DATA_ENCERRAMENTO = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return str(self.id)


