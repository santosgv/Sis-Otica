from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import connection
from Core.models import CLIENTE,ORDEN,SERVICO,LABORATORIO,Produto,CAIXA,Fornecedor,TipoUnitario,Estilo,Tipo
from Autenticacao.models import USUARIO

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        # Adiciona o tipo de plano do tenant no token
        tenant = connection.tenant
        token['tipo_plano'] = tenant.tipo_plano

        return token

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = USUARIO
        fields = ('id','username','first_name','FUNCAO')

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