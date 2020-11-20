from PIL import Image, ImageFont, ImageDraw
from django.core.files.storage import default_storage as s3_storage
import apps.email.sendMail
from apps.diseño.models import Diseño

# Permite transformar una imagen leyendola desde un bucket s3 de aws
def transformImage(diseño_id, diseño_original, nombre_diseñador, fecha):    
    target = '.png'
    size = 800, 600

    # Carpeta donde se dejan los archivos que no lograron ser convertidos a PNG
    # badFiles_directory = 'badfiles/' 

    # Carpeta con los archivos ya convertidos a .png
    processed_directory = 'procesados/'       

    try:
        # Buscar el diseño a procesar
        design = Diseño.objects.get(pk=diseño_id)
                
        # Leer la imagen del bucket s3 en el sistema        
        with s3_storage.open(diseño_original, 'rb') as s3_image:
            # Cargar la imagen como un objeto Pillow.Image
            im = Image.open(s3_image)
        
        # Operaciones sobre la imagen            
        im = im.resize(size, Image.ANTIALIAS)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(font='./apps/image/arialbd.ttf', size=20) 
        draw.text((10, 550), nombre_diseñador + ' - ' + fecha, (255), font=font)

        # Guardar la imagen procesada en el bucket s3
        with s3_storage.open(processed_directory + diseño_id + target, 'w') as s3_processed_image:
            im.save(s3_processed_image, optimize=True)

        # Guardar la referencia a la imagen procesada
        design.diseno_procesado = processed_directory + diseño_id + target
        design.estado = True
        design.save()

        # Enviar el correo notificando al diseñador que su diseño ya fue procesado
        apps.email.sendMail.sendMail(design.email_disenador, diseño_id, design.fecha_publicacion)
    except:
        # TODO: Intentar almacenar en el bucket badfiles o realizar una politica de almacenamiento local
        # para retry
        print(error)       



