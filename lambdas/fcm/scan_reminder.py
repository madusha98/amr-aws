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
stage = os.environ.get("stage")


def send_notifications(event, context):
    try:
        if offline == "true":
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')

        else:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('devicesTable-' + stage)
        data = table.scan()
        tokens = [item['pushToken'] for item in data['Items']]
        send_notification(tokens, 'Smart Scanner', 'Hello there, don\'t forget to scan your electricity meter before end of this month. Simply scan and pay the bill instantly!')
        
    except Exception as e:
        print('Exception: ', e)
        return {"error": str(e)}
    return ''