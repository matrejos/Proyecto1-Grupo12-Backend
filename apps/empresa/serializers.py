from rest_framework import serializers
from apps.empresa.models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    # Encadenar los proyectos de la empresa
    proyectos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Empresa
        fields = ['url', 'nombre', 'email', 'contraseña', 'proyectos']