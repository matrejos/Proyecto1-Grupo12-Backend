from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from backend.settings import SECRET_KEY
from backend.auth import authenticate
from apps.empresa.serializers import EmpresaSerializer
from apps.empresa.models import Empresa
import jwt
import datetime
import random

import bmemcached
import os
import environ

env = environ.Env()
env.read_env(env.str('ENV_PATH', '.env'))

servers = env('MEMCACHIER_SERVERS')
user = env('MEMCACHIER_USERNAME')
passw = env('MEMCACHIER_PASSWORD')

mc = bmemcached.Client(servers, username=user, password=passw)

mc.enable_retry_delay(True)

# Vistas

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def create_empresa(request, *args, **kwargs):    
    # Buscar el objeto de usuario para anexarle el evento       
    request_data = request.data.dict()
    # Anexar identificador propio
    identifier = str(random.randint(1,2409))
    if (request_data.get('nombre') is None):
        return JsonResponse({'message': 'El nombre de la empresa no ha sido proporcionado'}, status=400)    
    request_data['url'] = request_data.get('nombre').replace(' ', '-') + '-' + identifier
    serializer = EmpresaSerializer(data=request_data)
    if serializer.is_valid(): # Valida que los datos dados por el request sean validos
        serializer.save() # Guarda el objeto dado        
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def api_auth(request):    
    try:
        empresa = Empresa.objects.get(email=request.data['email'], contraseña=request.data['contraseña'])
    except Empresa.DoesNotExist:
        return JsonResponse({"message": "La empresa no existe o las credenciales suministradas no son validas"}, status=404)
    
    payload = {
        'username': request.data['email'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2, minutes=30)
    }
    token = mc.get(request.data['email'])
    if token == None:
        token = jwt.encode(payload, SECRET_KEY).decode('utf-8')
        mc.set(request.data['email'], token)
    return JsonResponse({'token': token, 'url': empresa.url}, status=200)

@api_view(['GET'])
@csrf_exempt
def get_all_business(request, *args, **kwargs):
    empresas = Empresa.objects.all()
    serializer = EmpresaSerializer(empresas, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@csrf_exempt
def get_business(request, business_id, *args, **kwargs):
    try:        
        empresa = Empresa.objects.get(url=business_id)        
    except Empresa.DoesNotExist:
        return JsonResponse({'message': 'La empresa no existe'}, status=404)        
    else:        
        serializer = EmpresaSerializer(empresa)
        return JsonResponse(serializer.data)
    

