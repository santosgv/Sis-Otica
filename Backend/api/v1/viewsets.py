from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from api.v1.serializers import ClientesSerializer,OrdensSerializer,UsuariosSerializer,ServicoSerializer,ProdutoSerializer,LaboratorioSerializer
from Core.models import CLIENTE,ORDEN,SERVICO,Produto,LABORATORIO
from Autenticacao.models import USUARIO
from Core.views import get_entrada_saida,vendas_ultimos_12_meses
from Core.utils import get_30_days,ultimo_dia_mes,get_10_days,get_today_data,dados_caixa

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
    
class UpdateCardStatusAPIView(APIView):
    def post(self, request, card_id):
        try:
            card = get_object_or_404(ORDEN, id=card_id)
            new_status = request.data.get('status')
            if not new_status:
                return Response(
                    {'error': 'O campo "status" é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 3. Atualizar o card
            card.STATUS = new_status
            card.save()
            
            # 4. Retornar apenas os dados necessários (sem tentar serializar o Response)
            return Response({
                'success': True,
                'message': 'Status atualizado com sucesso',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
