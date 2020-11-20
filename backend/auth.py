import jwt
from backend.settings import SECRET_KEY
from django.http import JsonResponse

# Permite validar el token del usuario para consumir los servicios del backend de acuerdo a sus 
# permisos. En caso de ser satisfactorio retorna el ID del usuario.
# Ingreso_registro: Bearer - Token

def authenticate(*args, **kwargs):    
    def decorator(function):
        def wrap(request, *args, **kwargs):            
            token = request.headers.get('Authorization')            
            if token is None:                
                msg = 'Invalid token header. No credentials provided.'
                return JsonResponse({'Error': msg}, status=401)
            try:
                token.encode('utf-8')
            except UnicodeError:                
                msg = 'Invalid token header. Token string should not contain invalid characters.'
                return JsonResponse({'Error': msg}, status=401)
            else:
                username = None
                try: 
                    token = token.strip().split(' ')[1]                     
                    payload = jwt.decode(token, SECRET_KEY)
                    username = payload['username']                    
                except jwt.DecodeError:            
                    msg = 'Invalid token provided'                    
                    return JsonResponse({'Error': msg}, status=401)
                except jwt.ExpiredSignatureError:
                    msg = 'Invalid token provided. The token has expired'                    
                    return JsonResponse({'Error': msg}, status=401)

                #Token Valido - Devolver el cuerpo    
                #El único elemento en la tupla es el nombre de usuario
                else:
                    args = (username)
                    kwargs['username'] = username
                    return function(request, *args, **kwargs)                                
        return wrap
    return decorator
