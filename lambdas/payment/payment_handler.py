import json
import boto3
import base64
from botocore.config import Config

def save_payment(event, context):
    statusCode = 200
    responseBody = {'data': ''}
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2') # local
    # dynamodb = boto3.resource('dynamodb')
    # body_dec = base64.b64decode(event['body'])
    # req = json.loads(body_dec)
    req = json.loads(event['body']) # Uncomment to run locally
    try:
        table = dynamodb.Table('paymentTable')
        resp = table.put_item(Item={
            'transactionId': req['transactionId'],
            'amount': req['amount'],
            'accNo': req['accNo'],
            'date': req['date']
        })
        responseBody = { "data": resp, "message": "Payment Saved Successfully" }

    except Exception as e:
        print('Exception: ', e)
        statusCode = 500
        responseBody = {"error": str(e) }

    response = {
        "statusCode": statusCode,
        "body": json.dumps(responseBody)
    }

    return response