from django.db import models
from apps.empresa.models import Empresa
import uuid

# Create your models here.
class Proyecto(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='proyectos', on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nombre = models.CharField(max_length=256)
    descripcion = models.CharField(max_length=256)
    valor = models.IntegerField()