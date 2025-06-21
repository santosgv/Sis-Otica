from rest_framework import routers
from api.v1.viewsets import ClientesViewSet,OrdensViewSet

router = routers.DefaultRouter()
router.register(r'clientes', ClientesViewSet)
router.register(r'ordens',OrdensViewSet)