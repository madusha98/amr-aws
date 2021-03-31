import requests
import json
import base64
import boto3
import uuid
import time
from botocore.config import Config
from decimal import Decimal


def get_bill_value(event, context):

    # 1. parse out request json body
    body_dec = base64.b64decode(event['body'])
    request = json.loads(body_dec)
    # request = json.loads(event['body'])
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

    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table('billTable')
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

    # 4. return the repsonse object
    response = json.loads(response.text)
    return {
        "body": json.dumps(response)
    }
    

