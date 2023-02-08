from django.db import models


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