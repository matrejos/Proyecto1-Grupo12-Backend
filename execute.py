import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] =  "backend.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import time
import django
django.setup()


from taskManager.tasks import processImages
from apps.diseño.models import Diseño
import boto3

def execute():
    sqs = boto3.client('sqs', region_name="us-east-1")
    queue_url = 'https://sqs.us-east-1.amazonaws.com/706608037047/HerokuQueue.fifo'
    while True:
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=25,
            WaitTimeSeconds=0
        )
        if 'Messages' in response:
            message = response['Messages'][0]
            diseno_original = message['Body']
            d = Diseño.objects.filter(diseno_original=diseno_original, estado=False)
            if len(d) > 0:
                d = d[0]
                processImages.delay(d.id, d.diseno_original.name, d.nombre_disenador + ' ' + d.apellido_disenador, d.fecha_publicacion)
            receipt_handle = message['ReceiptHandle']
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        #time.sleep(1)