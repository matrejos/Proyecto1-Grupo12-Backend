from django.db import models
from apps.proyecto.models import Proyecto
import uuid

# Determina el nombre del diseño y la ruta para almacenarlo
def save_process_design(instance, filename):
    fn = str(instance.id) + '.' + filename.split('.')[-1]    
    return 'proceso/{0}'.format(fn)

# Create your models here.
class Diseño(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='diseños', on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nombre_disenador = models.CharField(max_length=256)
    apellido_disenador = models.CharField(max_length=256)
    email_disenador = models.EmailField()
    fecha_publicacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=False)
    precio = models.IntegerField()
    # Cargar los modelos en el sistema
    diseno_original = models.ImageField(upload_to=save_process_design)
    diseno_procesado = models.ImageField()
