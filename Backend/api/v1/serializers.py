from rest_framework import serializers
from Core.models import CLIENTE,ORDEN,SERVICO,LABORATORIO,Produto,CAIXA,Fornecedor,TipoUnitario,Estilo,Tipo
from Autenticacao.models import USUARIO,Comissao, Desconto


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = USUARIO
        fields = ('id','username','first_name','FUNCAO','salario_bruto','comissao_percentual','valor_hora','data_contratacao')

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLIENTE
        fields= '__all__'
        extra_kwargs = {
            'DATA_CADASTRO': {'read_only': True},  
            'STATUS': {'read_only': True}
        }

class OrdensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ORDEN
        fields= '__all__'

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SERVICO
        fields = ('id','SERVICO')
        
class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LABORATORIO
        fields = ('id','LABORATORIO')

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        extra_kwargs = {
            'codigo': {'read_only': True},  
            'valor_total': {'read_only': True}
        }

class CaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CAIXA
        fields = '__all__'
        extra_kwargs = {
            'SALDO_FINAL':{'read_only':True}
        }

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ('id','nome')

class TipoUnitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUnitario
        fields = ('id','nome')

class EstiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estilo
        fields = ('id','nome')

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = ('id','nome')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ORDEN
        fields = [
            'id',
            'DATA_SOLICITACAO',
            'OBSERVACAO',
            'SERVICO',
            'VALOR',
            'FORMA_PAG'
        ]

class FolhaPagamentoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='colaborador.first_name')
    data_contratacao = serializers.DateField(source='colaborador.data_contratacao')
    salario_bruto = serializers.FloatField(source='colaborador.salario_bruto')
    comissao = serializers.SerializerMethodField()
    horas_extras = serializers.SerializerMethodField()
    descontos = serializers.SerializerMethodField()
    salario_liquido = serializers.SerializerMethodField()

    class Meta:
        model = Comissao
        fields = [
            'nome', 'data_contratacao', 'salario_bruto',
            'comissao', 'horas_extras', 'descontos', 'salario_liquido'
        ]

    def get_comissao(self, obj):
        print("Calculating commission for:", obj.colaborador.first_name)
        return obj.calcular_comissao()

    def get_horas_extras(self, obj):
        print("Calculating extra hours for:", obj.colaborador.first_name)
        return obj.calcula_horas_extras()

    def get_descontos(self, obj):
        descontos = obj.colaborador.desconto_set.all()
        return [
            {
                'tipo': d.tipo,
                'percentual': d.percentual,
                'valor': d.calcular_valor(),
            } for d in descontos
        ]

    def get_salario_liquido(self, obj):
        print("Calculating net salary for:", obj.colaborador.first_name)
        return obj.salario_liquido()

class ComissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comissao
        fields = '__all__'
class DescontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desconto
        fields = '__all__'