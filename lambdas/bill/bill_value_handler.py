import requests
import simplejson as json
import base64
import boto3
import uuid
import time
from botocore.config import Config
from decimal import Decimal
import os

offline = os.environ.get("IS_OFFLINE")
stage = os.environ.get("stage")


def get_bill_value(event, context):

    # 1. parse out request json body
    try:
        if offline == "true":
            request = json.loads(event['body'])
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
        else: 
            body_dec = base64.b64decode(event['body'])
            request = json.loads(body_dec)
            dynamodb = boto3.resource('dynamodb')
    except Exception as e:
        print('Exception: ', e)
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
            }

    noOfUnits = request['NoOfUnits']
    fromDate = request['FromDate']
    toDate = request['ToDate']

    # 2. construct the header and body of the CEB endpoint
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {'tariff_cat': '11',
            'iUnit': noOfUnits,
            'datepicker3': fromDate,
            'datepicker4': toDate,
            'lastsegment': 'en'}
    
    # 3. construct the http response from CEB endpoint
    response = requests.post(
        "https://ceb.lk/bill_calculation_commercial/calculate_bill", headers=headers, data=data, verify=False)

    # response_load = json.loads(response.text)
    # print('Bill Value:', response_load['Total'])

    try:
        table = dynamodb.Table('billTable-' + stage)
        id = uuid.uuid4().hex
        resp = table.put_item(Item={
                'billId': id,
                'readingId': request['readingId'],
                'accId': request['accId'],
                'billValue': json.loads(response.text),
                'date': Decimal(str(time.time()))
            })
    except Exception as e:
        print('Exception: ', e)
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
            }


    # 4. return the repsonse object
    response = json.loads(response.text)
    return {
        "body": json.dumps(response)
    }
    

