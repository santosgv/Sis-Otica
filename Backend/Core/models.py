from django.db import models
from django.db.models import Sum
from Autenticacao.models import USUARIO
from django.utils.timezone import now
from django.conf import settings
from simple_history.models import HistoricalRecords


def current_date():
    return now().date()

class CLIENTE(models.Model):

    CHOICES_SITUACAO=(
        ('1','ATIVO'),
        ('2','INATIVO')
    )
    

    NOME = models.CharField(max_length=250)
    LOGRADOURO = models.CharField(max_length=80)
    CEP = models.CharField(max_length=8)
    NUMERO = models.CharField(max_length=10)
    BAIRRO = models.CharField(max_length=200)
    CIDADE = models.CharField(max_length=200)
    TELEFONE = models.CharField(max_length=30, blank=True, null=True)
    CPF = models.CharField(max_length=14)
    DATA_NASCIMENTO = models.DateField(blank=True, null=True)
    EMAIL = models.CharField(max_length=100,blank=True, null=True)
    FOTO =  models.ImageField(upload_to='foto_img',blank=True, null=True)
    DATA_CADASTRO = models.DateTimeField(default=now)
    STATUS = models.CharField(max_length=1,choices=CHOICES_SITUACAO,default='1')

    def __str__(self) -> str:
        return str(self.NOME)
    
class SERVICO(models.Model):
    SERVICO = models.CharField(max_length=500)
    ATIVO = models.BooleanField(default=True)
    def __str__(self) -> str:
        return str(self.SERVICO)

class LABORATORIO(models.Model):
    LABORATORIO = models.CharField(max_length=500)
    ATIVO = models.BooleanField(default=True)
    def __str__(self) -> str:
        return str(self.LABORATORIO)       

class ORDEN(models.Model):

    CHOICES_SITUACAO =(
        ('A','SOLICITADO'),
        ('E','ENTREGUE'),
        ('C','CANCELADO'),
        ('L','LABORATÓRIO'),
        ('J','LOJA'),
        ('F','FINALIZADO')
    )

    CHOICES_PAGAMENTO =(
        ('A','PIX'),
        ('B','DINHEIRO'),
        ('C','DEBITO'),
        ('D','CREDITO'),
        ('E','CARNER'),
        ('F','PERMUTA'),
    )
    DATA_SOLICITACAO = models.DateField(default=current_date)
    STATUS = models.CharField(max_length=1 , choices=CHOICES_SITUACAO, default='A')
    ANEXO =  models.ImageField(upload_to='anexo_img' ,blank=True, null=True)
    VENDEDOR = models.ForeignKey(USUARIO, on_delete=models.DO_NOTHING)
    CLIENTE = models.ForeignKey(CLIENTE,on_delete=models.SET_NULL,null=True)
    PREVISAO_ENTREGA = models.DateField()
    ASSINATURA = models.ImageField(upload_to='assinatura_img' ,blank=True, null=True)
    SERVICO = models.ForeignKey(SERVICO, on_delete=models.DO_NOTHING)
    LABORATORIO = models.ForeignKey(LABORATORIO,on_delete=models.SET_NULL,null=True)
    OD_ESF = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OD_CIL = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OD_EIXO = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OE_ESF = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OE_CIL = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    OE_EIXO = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    AD = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    DNP = models.CharField(max_length=15,blank=True, null=True,default='N/D')
    P = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    DPA = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    DIAG = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    V = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    H = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    ALT = models.CharField(max_length=5,blank=True, null=True,default='N/D')
    ARM = models.CharField(max_length=50,blank=True, null=True,default='N/D')
    MONTAGEM = models.CharField(max_length=50,blank=True, null=True,default='N/D')
    LENTES = models.CharField(max_length=500,blank=True, null=True,default='N/D')
    ARMACAO = models.CharField(max_length=500, blank=True, null=True,default='N/D')
    OBSERVACAO = models.TextField(max_length=1000, blank=True, null=True,default='N/D')
    FORMA_PAG = models.CharField(max_length=1, choices=CHOICES_PAGAMENTO,blank=True, null=True,default='N/D')
    VALOR =  models.DecimalField(max_digits=10, decimal_places=2)
    QUANTIDADE_PARCELA = models.IntegerField(blank=True, null=True,default='N/D')
    ENTRADA = models.CharField(max_length=100)
    DATA_ENCERRAMENTO = models.DateTimeField(blank=True, null=True)
    history = HistoricalRecords()
    

    def __str__(self):
        return str(self.id)
    
    def solicitar_avaliacao(self):
        """Retorna True se o cliente ainda não foi avaliado após o pedido finalizado."""
        if self.STATUS == 'E':
            return not Review.objects.filter(cliente=self.CLIENTE).exists()
        return False
    
class CAIXA(models.Model):

    CHOICES_PAGAMENTO =(
        ('A','PIX'),
        ('B','DINHEIRO'),
        ('C','DEBITO'),
        ('D','CREDITO'),
        ('E','CARNER'),
        ('F','PERMUTA'),
    )

    CHOICES_TIPO= (
        ('E','Entrada'),
        ('S','Saida')
    )

    DATA =models.DateField(default=now)
    DESCRICAO = models.CharField(max_length=255, blank=True)
    REFERENCIA = models.ForeignKey(ORDEN, blank=True ,on_delete=models.SET_NULL,null=True)
    TIPO = models.CharField(max_length=1, choices=CHOICES_TIPO, default="E")
    VALOR = models.FloatField()
    FORMA = models.CharField(max_length=1, choices=CHOICES_PAGAMENTO, default="B")
    FECHADO = models.BooleanField(default=False)
    SALDO_FINAL =models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.id)
    
    def fechar_caixa(self):
        self.FECHADO = True
        return

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100, db_index=True)


    def __str__(self) -> str:
        return str(self.nome)

    class Meta:
        verbose_name = 'Fornecedores'
        verbose_name_plural = 'Fornecedores'

class TipoUnitario(models.Model):
    nome = models.CharField(max_length=50 ,db_index=True)

    def __str__(self) -> str:
        return str(self.nome)
    
class Estilo(models.Model):
    nome = models.CharField(max_length=50 ,db_index=True)

    class Meta:
        verbose_name = 'Estilo'
        verbose_name_plural = 'Estilos'

    def __str__(self) -> str:
        return str(self.nome)
    
class Tipo(models.Model):
    nome = models.CharField(max_length=50, db_index=True)


    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self) -> str:
        return str(self.nome)

class Produto(models.Model):
    importado =models.BooleanField(default=False)
    conferido =models.BooleanField(default=False)
    chavenfe= models.CharField(max_length=44, unique=True,null=True, blank=True)
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    Tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    Estilo = models.ForeignKey(Estilo, on_delete=models.CASCADE)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    quantidade_minima = models.PositiveIntegerField()
    tipo_unitario = models.ForeignKey(TipoUnitario, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    def registrar_entrada(self, quantidade):
        self.quantidade += quantidade
        self.save()

    def registrar_saida(self, quantidade):
        if quantidade <= self.quantidade:
            self.quantidade -= quantidade
            self.save()
            return True
        else:
            return False

    def calcular_total(self):
        return self.quantidade * self.preco_unitario
    
    def save(self, *args, **kwargs):
        fornecedor_nome = self.fornecedor.nome
        primeira_letra = fornecedor_nome[0]
        ultima_letra = fornecedor_nome[-1]
        self.codigo =f"{self.nome}-{primeira_letra}{ultima_letra}-{settings.UNIDADE}{self.fornecedor.pk}{self.Tipo.pk}{self.Estilo.pk}"
        self.valor_total = self.calcular_total()
        
        # Verificar se o campo valor_total está vazio
        if self.pk is None and self.valor_total is None:
            self.valor_total = 0
        
        # Salvar o objeto
        super().save(*args, **kwargs)

        
    def __str__(self) -> str:
        return str(self.nome)

class EntradaEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entrada Estoque'
        verbose_name_plural = 'Entrada Estoque'

class SaidaEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    observacao= models.CharField(max_length=100,null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Saida Estoque'
        verbose_name_plural = 'Saida Estoque'

class MovimentoEstoque(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimentaçao'
        verbose_name_plural = 'Movimentaçao'

class AlertaEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    mensagem = models.CharField(max_length=255)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return self.mensagem
    
class Review(models.Model):
    cliente = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, related_name="reviews")
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(default=now)

    def __str__(self):
        return f"Avaliação {self.nota} - {self.cliente.NOME}"