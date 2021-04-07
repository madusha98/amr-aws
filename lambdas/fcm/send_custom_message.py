import requests
import simplejson as json
import base64
import boto3
import time
from botocore.config import Config
from decimal import Decimal
import os
try:
    from push_message_handler import send_notification
except Exception as e:
    from lambdas.fcm.push_message_handler import send_notification

offline = os.environ.get("IS_OFFLINE")


def send_notifications(event, context):
    try:
        if offline == "true":
            request = json.loads(event['body'])
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')

        else:
            dynamodb = boto3.resource('dynamodb')
            body_dec = base64.b64decode(event['body'])
            request = json.loads(body_dec)

        table = dynamodb.Table('devicesTable')
        data = table.scan()
        data = table.scan()
        tokens = [item['pushToken'] for item in data['Items']]
        send_notification(tokens, request['title'], request['message'])

        return {'body': {
            'message': 'Notifications sent successfully'
            }}
        
    except Exception as e:
        print('Exception: ', e)
        return {"error": str(e)}
    