from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from backend.settings import SECRET_KEY
from backend.auth import authenticate
from apps.proyecto.serializers import ProyectoSerializer
from apps.proyecto.models import Proyecto
from apps.empresa.models import Empresa

@csrf_exempt
def project_list(request, business_id="", *args, **kwargs):
    print("[Project] Business ID", business_id)
    kwargs['business_id'] = business_id

    if request.method == 'POST':
        return create_project(request, *args, **kwargs)
    elif request.method == 'GET':
        return get_business_projects(request, *args, **kwargs)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
@authenticate()
def create_project(request, *args, **kwargs):
    # Buscar el objeto de usuario para anexarle el proyecto
    request_data = request.data.dict()
    request_data['empresa'] = kwargs['username'] # Asociar con la empresa dada su pk (email) 
    print("Email de la empresa", request_data['empresa'])                           
    serializer = ProyectoSerializer(data=request_data)
    if serializer.is_valid(): # Valida que los datos dados por el request sean validos
        serializer.save() # Guarda el objeto dado        
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@parser_classes([MultiPartParser])
@csrf_exempt
def get_business_projects(request, *args, **kwargs): 
    print("[Proyectos] Proyectos de la empresa", kwargs['business_id'])  
    business = Empresa.objects.get(url=kwargs['business_id'])      
    projects = Proyecto.objects.filter(empresa=business.email)
    serializer = ProyectoSerializer(projects, many=True)
    return JsonResponse(serializer.data, safe=False) 

@csrf_exempt
def project_detail(request, proyecto_pk, business_id="", *args, **kwargs):
    #Guardar el PK en el diccionario de parametros opcionales
    #Al pasar por el decorador, el parametro se pierde y queda asignado pura basura logica
    kwargs['pk'] = proyecto_pk  
    kwargs['business_id'] = business_id  

    if request.method == 'GET':
        return project_detail_get(request, *args, **kwargs)
    elif request.method == 'PUT':
        return project_detail_put(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return project_detail_delete(request, *args, **kwargs)

@api_view(['GET'])
@csrf_exempt
def project_detail_get(request, *args, **kwargs):        
    try:
        business = Empresa.objects.get(url=kwargs['business_id'])            
        project = Proyecto.objects.get(empresa=business.email, pk=kwargs['pk'])        
    except Proyecto.DoesNotExist:
        return JsonResponse({'message': 'El proyecto no existe'}, status=404)        
    else:
        print("El proyecto existe")        
        serializer = ProyectoSerializer(project)
        return JsonResponse(serializer.data)

@api_view(['PUT'])
@parser_classes([MultiPartParser])
@csrf_exempt
@authenticate()
def project_detail_put(request, *args, **kwargs):
    try:     
        project = Proyecto.objects.get(empresa=kwargs['username'], pk=kwargs['pk']) 
        serializer = ProyectoSerializer(project, data=request.data, partial=True)
        if serializer.is_valid(): #Valida que los datos dados por el request sean validos
            serializer.save() #Guarda el objeto dado
            return JsonResponse(serializer.data, status=202)
        return JsonResponse(serializer.errors, status=400)
    except Proyecto.DoesNotExist:
        return JsonResponse({'message': 'El proyecto no existe'}, status=404)

@api_view(['DELETE'])
@csrf_exempt
@authenticate()
def project_detail_delete(request, *args, **kwargs): 
    try:
        project = Proyecto.objects.get(empresa=kwargs['username'], pk=kwargs['pk'])
        serializer = ProyectoSerializer(project)
        copy = serializer.data
        project.delete()
        return JsonResponse(copy, safe=False)
    except Proyecto.DoesNotExist:
        return JsonResponse({'message': 'El proyecto no existe'}, status=404)
