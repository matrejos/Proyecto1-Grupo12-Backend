from django.db import models

# Create your models here.
class Empresa(models.Model):
    url = models.CharField(max_length=256)
    nombre = models.CharField(max_length=256)
    email = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=256)
    
