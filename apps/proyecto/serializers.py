from rest_framework import serializers
from apps.proyecto.models import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    # Encadenar los diseños del proyecto
    diseños = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'valor', 'empresa', 'diseños']



        