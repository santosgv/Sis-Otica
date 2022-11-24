from django.db import models

class UNIDADE(models.Model):
    NOME = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.NOME)

class FUNCIONARIO(models.Model):

    CHOICES_SITUACAO =((
        'A','Ativo',
        'F','Ferias',
        'I','Inativo'
    ))

    CHOICES_FUNCAO =((
        'V','Vendedor',
        'C','Caixa',
        'G','Gerente'
    ))

    NOME = models.CharField(max_length=100)
    CPF = models.CharField(blank=True, max_length=18)
    DATA_NASCIMENTO = models.TimeField()
    SITUACAO = models.CharField(max_length=1,choices=CHOICES_SITUACAO,default="A")
    FUNCAO = models.CharField(max_length=1)

    def __str__(self) -> str:
        return str(self.NOME)

class FUNCIONARIO_UNIDADE(models.Model):
    FUNCIONARIO = models.ForeignKey(FUNCIONARIO,on_delete=models.DO_NOTHING)
    UNIDADE = models.ForeignKey(UNIDADE,on_delete=models.DO_NOTHING)