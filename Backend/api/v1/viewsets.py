from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from api.v1.serializers import ClientesSerializer,OrdensSerializer,UsuariosSerializer,ServicoSerializer,ProdutoSerializer,LaboratorioSerializer
from Core.models import CLIENTE,ORDEN,SERVICO,Produto,LABORATORIO
from Autenticacao.models import USUARIO
from Core.utils import get_30_days,ultimo_dia_mes,get_10_days,get_today_data

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = USUARIO.objects.filter()
    serializer_class = UsuariosSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = CLIENTE.objects.filter(STATUS=1)
    serializer_class = ClientesSerializer

class OrdensViewSet(viewsets.ModelViewSet):
    queryset = ORDEN.objects.all()
    serializer_class = OrdensSerializer

class ServicosViewSet(viewsets.ModelViewSet):
    queryset = SERVICO.objects.filter(ATIVO=True)
    serializer_class = ServicoSerializer

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class LaboratoriosViewSet(viewsets.ModelViewSet):
    queryset = LABORATORIO.objects.filter(ATIVO=True)
    serializer_class = LaboratorioSerializer


class KanbanAPIView(APIView):
    def get(self, request):
        # Filtros equivalentes aos da view original
        solicitado = ORDEN.objects.filter(
            DATA_SOLICITACAO__gte=get_30_days(),
            DATA_SOLICITACAO__lte=ultimo_dia_mes(),
            STATUS='A'
        ).order_by('id')
        
        laboratorio = ORDEN.objects.filter(
            DATA_SOLICITACAO__gte=get_30_days(),
            DATA_SOLICITACAO__lte=ultimo_dia_mes(),
            STATUS='L'
        ).order_by('id')
        
        loja = ORDEN.objects.filter(
            DATA_SOLICITACAO__gte=get_30_days(),
            DATA_SOLICITACAO__lte=ultimo_dia_mes(),
            STATUS='J'
        ).order_by('id')
        
        entregue = ORDEN.objects.filter(
            DATA_SOLICITACAO__gte=get_10_days(),
            DATA_SOLICITACAO__lte=get_today_data(),
            STATUS='E'
        ).order_by('id')

        # Serialização básica (você pode criar um Serializer mais elaborado depois)
        def serialize_queryset(qs):
            return [{
                'id': item.id,
                'data_solicitacao': item.DATA_SOLICITACAO,
                'status': item.STATUS,
                # Adicione outros campos necessários
            } for item in qs]

        return Response({
            'solicitado': OrdensSerializer(solicitado,many=True).data,
            'laboratorio': OrdensSerializer(laboratorio,many=True).data,
            'loja': OrdensSerializer(loja,many=True).data,
            'entregue': OrdensSerializer(entregue,many=True).data,
            'metadata': {
                'total_solicitado': solicitado.count(),
                'total_laboratorio': laboratorio.count(),
                'total_loja': loja.count(),
                'total_entregue': entregue.count(),
            }
        })