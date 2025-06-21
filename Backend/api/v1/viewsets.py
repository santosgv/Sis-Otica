from rest_framework import viewsets
from api.v1.serializers import ClientesSerializer,OrdensSerializer
from Core.models import CLIENTE,ORDEN


class ClientesViewSet(viewsets.ModelViewSet):
    queryset = CLIENTE.objects.all()
    serializer_class = ClientesSerializer


class OrdensViewSet(viewsets.ModelViewSet):
    queryset = ORDEN.objects.all()
    serializer_class = OrdensSerializer