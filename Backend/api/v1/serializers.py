from rest_framework import serializers
from Core.models import CLIENTE,ORDEN

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLIENTE
        fields= '__all__'

class OrdensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ORDEN
        fields= '__all__'