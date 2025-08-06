from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from calendar import monthrange
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from api.v1.serializers import (CustomTokenObtainPairSerializer,ClientesSerializer,OrdensSerializer,UsuariosSerializer,
                                ServicoSerializer,ProdutoSerializer,LaboratorioSerializer,
                                CaixaSerializer,FornecedorSerializer,TipoUnitarioSerializer,
                                EstiloSerializer,TipoSerializer,PedidoSerializer,FolhaPagamentoSerializer,
                                ComissaoSerializer,DescontoSerializer)
from Core.models import CLIENTE,ORDEN,SERVICO,Produto,LABORATORIO,CAIXA,Fornecedor,TipoUnitario,Estilo,Tipo
from Autenticacao.models import USUARIO,Comissao,Desconto
from django.db.models import Sum,Count, F, ExpressionWrapper, DecimalField
from Core.utils import get_30_days,ultimo_dia_mes,get_today_data,primeiro_dia_mes
from django.utils.dateparse import parse_date

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UsuariosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = USUARIO.objects.filter().order_by('-id')
    serializer_class = UsuariosSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CLIENTE.objects.all().order_by('-id')
    serializer_class = ClientesSerializer

class OrdensViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ORDEN.objects.all().order_by('-id')
    serializer_class = OrdensSerializer

class ServicosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SERVICO.objects.filter(ATIVO=True).order_by('-id')
    serializer_class = ServicoSerializer

class ProdutosViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Produto.objects.all().order_by('-id')
    serializer_class = ProdutoSerializer

class LaboratoriosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LABORATORIO.objects.filter(ATIVO=True).order_by('-id')
    serializer_class = LaboratorioSerializer

class KanbanAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
            DATA_SOLICITACAO__gte=get_30_days(),
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
    permission_classes = [IsAuthenticated]
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

class CaixaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CAIXA.objects.all().order_by('-id')
    serializer_class = CaixaSerializer

class FechamentoCaixaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            # Último caixa fechado (em dinheiro)
            ultimo_caixa_fechado = CAIXA.objects.filter(FECHADO=True, FORMA='B').order_by('DATA').last()
            saldo_anterior = ultimo_caixa_fechado.SALDO_FINAL if ultimo_caixa_fechado else 0

            # Entradas e saídas do mês atual (em dinheiro)
            entradas = CAIXA.objects.filter(
                DATA__gte=primeiro_dia_mes(),
                DATA__lte=ultimo_dia_mes(),
                TIPO='E', FORMA='B', FECHADO=False
            ).aggregate(Sum('VALOR'))['VALOR__sum'] or 0

            saidas = CAIXA.objects.filter(
                DATA__gte=primeiro_dia_mes(),
                DATA__lte=ultimo_dia_mes(),
                TIPO='S', FORMA='B', FECHADO=False
            ).aggregate(Sum('VALOR'))['VALOR__sum'] or 0

            saldo = round(entradas - saidas, 2)
            saldo_total_dinheiro = saldo + saldo_anterior

            entradas_total = CAIXA.objects.filter(
                DATA__gte=primeiro_dia_mes(),
                DATA__lte=ultimo_dia_mes(),
                TIPO='E', FECHADO=False
            ).aggregate(Sum('VALOR'))['VALOR__sum'] or 0

            return Response({
                'entrada': entradas,
                'saida': saidas,
                'saldo_total_dinheiro': saldo_total_dinheiro,
                'entradas_total': entradas_total
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DadosCaixaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = CAIXA.objects.filter(
            DATA__gte=primeiro_dia_mes(),
            DATA__lte=ultimo_dia_mes(),
            FECHADO=False
        ).order_by('-id')

        serializer = CaixaSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CaixaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        PUT requer um ID no corpo ou pode ser implementado com a rota /api/dados-caixa/<pk>/
        """
        try:
            caixa_id = pk or request.data.get('id')
            caixa = CAIXA.objects.get(id=caixa_id)
        except CAIXA.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CaixaSerializer(caixa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FornecedorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Fornecedor.objects.all().order_by('-id')
    serializer_class = FornecedorSerializer

class TipoUnitarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TipoUnitario.objects.all().order_by('-id')
    serializer_class = TipoUnitarioSerializer

class EstiloViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Estilo.objects.all().order_by('-id')
    serializer_class = EstiloSerializer

class TipoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tipo.objects.all().order_by('-id')
    serializer_class = TipoSerializer

class MinhasVendasAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            id_user = request.user.id
            data_inicio = request.GET.get("data_inicio")
            data_fim = request.GET.get("data_fim")

            data_inicio_data = parse_date(data_inicio)
            data_fim_data = parse_date(data_fim)

            vendedor = ORDEN.objects.filter(
                DATA_SOLICITACAO__gte=data_inicio_data,
                DATA_SOLICITACAO__lte=data_fim_data,
                VENDEDOR__id=id_user
            ).exclude(STATUS='C') \
            .values('VENDEDOR__first_name') \
            .annotate(total_pedidos=Count('id')) \
            .annotate(total_valor_vendas=Sum('VALOR')) \
            .annotate(ticket_medio=ExpressionWrapper(
                F('total_valor_vendas') / F('total_pedidos'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )) \
            .order_by('-total_pedidos')[:1]

            return Response({'minhas_vendas_mes': list(vendedor)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PedidosDoVendedorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user.id
        data_inicio = request.GET.get("data_inicio")
        data_fim = request.GET.get("data_fim")

        response = Response()


        if not data_inicio or not data_fim:
            response.data = {"erro": "Parâmetros data_inicio e data_fim são obrigatórios."}
            response.status_code = 400
            return response

        try:
            data_inicio = parse_date(data_inicio)
            data_fim = parse_date(data_fim)
        except ValueError:
            response.data = {"erro": "Formato de data inválido."}
            response.status_code = 400
            return response

        pedidos = ORDEN.objects.filter(
            DATA_SOLICITACAO__gte=data_inicio,
            DATA_SOLICITACAO__lte=data_fim,
            VENDEDOR__id=user
        ).exclude(STATUS='C').order_by("-DATA_SOLICITACAO")

        serializer = PedidoSerializer(pedidos, many=True)
        response.data = {"pedidos": serializer.data}
        return response

class DadosCaixaAnteriorApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data_inicio = request.GET.get("data_inicio")
        data_fim = request.GET.get("data_fim")
        response = Response()


        if not data_inicio or not data_fim:
            response.data = {"erro": "Parâmetros data_inicio e data_fim são obrigatórios."}
            response.status_code = 400
            return response

        entradas = CAIXA.objects.filter(
        DATA__range=(data_inicio, data_fim),
        FECHADO=True)
        
        serializer = CaixaSerializer(entradas, many=True)
        response.data = {"results": serializer.data}
        return response

class LojaOsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_os):
        try:
            loja_os = ORDEN.objects.get(id=id_os)
            loja_os.STATUS = "J"
            loja_os.save()
            return Response(
                    {"message": "O.S. foi movida para a loja com sucesso"},
                    status=200
                )
        except ORDEN.DoesNotExist:
            return Response({"error": "OS não encontrada."}, status=404)
        except Exception as e:

            return Response({"error": "Erro ao mover OS para a loja."}, status=500)

class EncerrarOsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_os):
        try:
            loja_os = ORDEN.objects.get(id=id_os)
            loja_os.STATUS = "F"
            loja_os.save()
            return Response(
                    {"message": "O.S. foi movida para a Encerrada com sucesso"},
                    status=200
                )
        except ORDEN.DoesNotExist:
            return Response({"error": "OS não encontrada."}, status=404)
        except Exception as e:
            print(e)
            return Response({"error": "Erro ao mover OS para a Encerrada."}, status=500)

class EntregueOsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_os):
        try:
            loja_os = ORDEN.objects.get(id=id_os)
            loja_os.STATUS = "E"
            loja_os.save()
            return Response(
                    {"message": "O.S. foi movida para a Entregue com sucesso"},
                    status=200
                )
        except ORDEN.DoesNotExist:
            return Response({"error": "OS não encontrada."}, status=404)
        except Exception as e:
            print(e)
            return Response({"error": "Erro ao mover OS para a Entregue."}, status=500)

class CanceladoOsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_os):
        try:
            loja_os = ORDEN.objects.get(id=id_os)
            loja_os.STATUS = "C"
            loja_os.save()
            return Response(
                    {"message": "O.S. foi movida para a Cancelado com sucesso"},
                    status=200
                )
        except ORDEN.DoesNotExist:
            return Response({"error": "OS não encontrada."}, status=404)
        except Exception as e:
            print(e)
            return Response({"error": "Erro ao mover OS para a Cancelado."}, status=500)

class LaboratorioOsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id_os):
        try:
            loja_os = ORDEN.objects.get(id=id_os)
            loja_os.STATUS = "L"
            loja_os.save()
            return Response(
                    {"message": "O.S. foi movida para a Laboratorio com sucesso"},
                    status=200
                )
        except ORDEN.DoesNotExist:
            return Response({"error": "OS não encontrada."}, status=404)
        except Exception as e:
            print(e)
            return Response({"error": "Erro ao mover OS para a Laboratorio."}, status=500)

class FolhaPagamentoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, usuario_id, referencia):
        try:

            partes = referencia.split('-')
            if len(partes) != 2:
                return Response({"error": "Formato de referência inválido. Use AAAA-MM."}, status=status.HTTP_400_BAD_REQUEST)

            ano = int(partes[0])
            mes = int(partes[1])
            primeiro_dia = date(ano, mes, 1)
            ultimo_dia = date(ano, mes, monthrange(ano, mes)[1])

            colaborador = get_object_or_404(USUARIO, id=usuario_id)

            comissoes = Comissao.objects.filter(
                colaborador=colaborador,
                data_referencia__range=(primeiro_dia, ultimo_dia)
            )
            if not comissoes.exists():
                total_comissao = 0
                total_horas = 0
                proventos = []

            descontos = Desconto.objects.filter(colaborador=colaborador)

            # Detalhes de comissão e hora extra
            comissoes_detalhadas = []
            total_comissao = 0
            total_horas_extras = 0
            for c in comissoes:
                valor_comissao = c.calcular_comissao()
                valor_horas = c.calcula_horas_extras()
                total_comissao += valor_comissao
                total_horas_extras += valor_horas
                comissoes_detalhadas.append({
                    "valor_vendas": c.valor_vendas,
                    "percentual": colaborador.comissao_percentual,
                    "comissao_gerada": round(valor_comissao, 2),
                    "horas_extras": c.horas_extras,
                    "valor_hora": colaborador.valor_hora,
                    "horas_extras_valor": round(valor_horas, 2)
                })

            # Detalhes dos descontos
            descontos_data = []
            total_descontos = 0
            for d in descontos:
                valor_desconto = colaborador.salario_bruto * (d.percentual / 100)
                total_descontos += valor_desconto
                descontos_data.append({
                    "tipo": d.tipo,
                    "percentual": f"{d.percentual}%",
                    "valor": round(valor_desconto, 2)
                })

            # Descontos fixos
            inss = round(colaborador.salario_bruto * 0.075, 2)
            fgts = round(colaborador.salario_bruto * 0.08, 2)
            irrf = 0  # Pode aplicar lógica futura
            total_descontos += inss + fgts + irrf

            folha = {
                "id": colaborador.id,
                "nome": colaborador.first_name,
                "funcao": colaborador.FUNCAO,
                "data_contratacao": colaborador.data_contratacao,
                "salario_bruto": round(colaborador.salario_bruto, 2),
                "descontos": descontos_data,
                "desconto_inss": inss,
                "desconto_fgts": fgts,
                "desconto_irrf": irrf,
                "total_descontos": round(total_descontos, 2),
                "proventos": comissoes_detalhadas,
                "total_comissao": round(total_comissao, 2),
                "total_horas": round(total_horas_extras, 2),
                "salario_liquido": round(
                    colaborador.salario_bruto + total_comissao + total_horas_extras - total_descontos,
                    2
                )
            }

            return Response(folha, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ComissaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comissao.objects.all().order_by('-id')
    serializer_class = ComissaoSerializer

class DescontoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Desconto.objects.all().order_by('-id')
    serializer_class = DescontoSerializer