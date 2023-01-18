from django.db import models
from django.utils.timezone import now



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
    VENCIMENTO = models.DateField()
    FORMA = models.CharField(max_length=1, choices=CHOICES_FORMA, default="M")
    PERIODO =models.IntegerField()

    def __str__(self) -> str:
        return str(self.CONTA)

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

    def __str__(self):
        return str(self.id)

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

    def __str__(self):
        return str(self.id)

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

