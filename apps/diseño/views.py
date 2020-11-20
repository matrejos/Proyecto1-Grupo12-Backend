from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage as s3_storage
from django.http import JsonResponse
from apps.diseño.serializers import DiseñoSerializer
from apps.diseño.models import Diseño
from apps.proyecto.models import Proyecto
from backend.settings import MEDIA_ROOT
import base64
import os
import boto3

sqs = boto3.client('sqs', region_name="us-east-1")
queue_url = 'https://sqs.us-east-1.amazonaws.com/706608037047/HerokuQueue.fifo'
# Codificar una imagen a base64
def encode_image(path):
    with s3_storage.open(path, "rb") as image_file:
        encode = base64.b64encode(image_file.read())
        # Parse to UTF-8
        return encode.decode('utf-8')

@csrf_exempt
def design_list(request, proyecto_pk, *args, **kwargs):    
    if request.method == 'POST':
        return create_design(request, proyecto_pk, args)
    elif request.method == 'GET':
        return get_project_designs(request, proyecto_pk, args)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def create_design(request, proyecto_pk, *args, **kwargs):    
    design = request.data.dict()
    design['proyecto'] = str(proyecto_pk)    
    serializer = DiseñoSerializer(data=design)
    if serializer.is_valid(): # Valida que los datos dados por el request sean validos
        serializer.save() # Guarda el objeto dado
        ruta = serializer.data['diseno_original'].split("/")[4]
        ruta = 'proceso/'+ruta.split("?")[0]
        sqs.send_message(
            QueueUrl=queue_url,
            MessageDeduplicationId='Dep1',
            MessageGroupId="Grupo1",
            MessageBody=ruta
        )
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@parser_classes([MultiPartParser])
@csrf_exempt
def get_project_designs(request, proyecto_pk, *args, **kwargs):
    design = Diseño.objects.filter(proyecto=proyecto_pk)
    serializer = DiseñoSerializer(design, many=True)
    return JsonResponse(serializer.data, safe=False) 

@csrf_exempt
def design_detail(request, proyecto_pk, design_pk, *args, **kwargs):    
    print("[Diseño] Acceso mediante el detalle")
    kwargs['design_pk'] = design_pk     
    kwargs['project_pk'] = proyecto_pk     

    if request.method == 'GET':
        return design_detail_get(request, *args, **kwargs)
    elif request.method == 'PUT':
        return design_detail_put(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return design_detail_delete(request, *args, **kwargs)

@api_view(['GET'])
@parser_classes([MultiPartParser])
@csrf_exempt
def design_detail_get(request, *args, **kwargs):      
    try:        
        design = Diseño.objects.get(proyecto=kwargs['project_pk'], pk=kwargs['design_pk'])        
    except Diseño.DoesNotExist:
        return JsonResponse({'message': 'El diseño no existe'}, status=404)        
    else:
        encode_original = ''
        encode_procesado = ''
        if len(design.diseno_procesado.name) != 0:
            encode_procesado = encode_image(design.diseno_procesado.name)        
        encode_original = encode_image(design.diseno_original.name)
        serializer = DiseñoSerializer(design)
        data = {**dict(serializer.data), **{'diseno_original': encode_original, 'diseno_procesado': encode_procesado}}
        return JsonResponse(data)

@api_view(['PUT'])
@parser_classes([MultiPartParser])
@csrf_exempt
def design_detail_put(request, *args, **kwargs):
    try:             
        request_data = request.data.dict() 
        design = Diseño.objects.get(proyecto=kwargs['project_pk'], pk=kwargs['design_pk'])                    
        serializer = DiseñoSerializer(design, data=request_data, partial=True)
        if serializer.is_valid(): #Valida que los datos dados por el request sean validos
            serializer.save() #Guarda el objeto dado
            return JsonResponse(serializer.data, status=202)
        return JsonResponse(serializer.errors, status=400)
    except Diseño.DoesNotExist:
        return JsonResponse({'message': 'El diseño no existe'}, status=404)        

@api_view(['DELETE'])
@parser_classes([MultiPartParser])
@csrf_exempt
def design_detail_delete(request, *args, **kwargs): 
    try:        
        design = Diseño.objects.get(proyecto=kwargs['project_pk'], pk=kwargs['design_pk']) 
        serializer = DiseñoSerializer(design)
        copy = serializer.data
        design.delete()
        return JsonResponse(copy, safe=False)
    except Diseño.DoesNotExist:
        return JsonResponse({'message': 'El diseño no existe'}, status=404)        