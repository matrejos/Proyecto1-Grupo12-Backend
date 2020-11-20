# Create your tasks here

from celery import shared_task
import apps.image.imageConvert
import apps.email.sendMail

@shared_task
def processImages(diseño_id, diseño_original, nombre_diseñador, fecha):
   apps.image.imageConvert.transformImage(diseño_id, diseño_original, nombre_diseñador, fecha)
   
@shared_task
def sendMail(to,  nombreDiseno,  fechaDiseno):
   apps.image.sendMail.sendMail(to,  nombreDiseno,  fechaDiseno)
