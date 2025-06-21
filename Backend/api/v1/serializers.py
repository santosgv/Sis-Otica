from rest_framework import serializers
from Core.models import CLIENTE,ORDEN,SERVICO,LABORATORIO,Produto
from Autenticacao.models import USUARIO


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = USUARIO
        fields = ('id','username','first_name','FUNCAO')

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLIENTE
        fields= '__all__'

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
