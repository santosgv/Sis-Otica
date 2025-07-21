from rest_framework import routers
from api.v1.viewsets import (ClientesViewSet,OrdensViewSet,UsuariosViewSet,
                            ServicosViewSet,ProdutosViewSet,LaboratoriosViewSet,
                            CaixaViewSet,FornecedorViewSet,TipoUnitarioViewSet,
                            EstiloViewSet,TipoViewSet, ComissaoViewSet,
                            DescontoViewSet)

router = routers.DefaultRouter()
router.register(r'clientes', ClientesViewSet)
router.register(r'ordens',OrdensViewSet)
router.register(f'usuarios',UsuariosViewSet)
router.register(f'servicos',ServicosViewSet)
router.register(f'produtos',ProdutosViewSet)
router.register(f'laboratorios',LaboratoriosViewSet)
router.register(f'caixa',CaixaViewSet)
router.register(f'fornecedor',FornecedorViewSet)
router.register(f'tipounitario',TipoUnitarioViewSet)
router.register(f'estilo',EstiloViewSet)
router.register(f'tipo',TipoViewSet)
router.register(f'comissoesapi', ComissaoViewSet, basename='comissoesapi')
router.register(f'descontos', DescontoViewSet, basename='descontos')
