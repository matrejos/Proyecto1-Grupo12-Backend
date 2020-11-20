from rest_framework import serializers
from apps.diseño.models import Diseño

class DiseñoSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Diseño
        fields = ['id', 'nombre_disenador', 'apellido_disenador', 'precio', 'email_disenador', 'fecha_publicacion', 'estado', 'diseno_original', 'proyecto']