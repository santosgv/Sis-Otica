from rest_framework import routers
from api.v1.viewsets import ClientesViewSet,OrdensViewSet,UsuariosViewSet,ServicosViewSet,ProdutosViewSet,LaboratoriosViewSet

router = routers.DefaultRouter()
router.register(r'clientes', ClientesViewSet)
router.register(r'ordens',OrdensViewSet)
router.register(f'usuarios',UsuariosViewSet)
router.register(f'servicos',ServicosViewSet)
router.register(f'produtos',ProdutosViewSet)
router.register(f'laboratorios',LaboratoriosViewSet)
