# import counter_recognition
import json
import uuid
import time
import boto3
import base64
from botocore.config import Config
from decimal import Decimal

def read_digits(event, context):

  # dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2') $ local
  dynamodb = boto3.resource('dynamodb')

  value = counter_recognition.get_reading(event)
  try:
    id = uuid.uuid4().hex
    item = {
      "readingId": id,
      "value": value['value'],
      "score": value['score'],
      "date": Decimal(str(time.time())),
      "accId": event["queryStringParameters"]['accId'],
      "imageUrl": "google.lk"
    }
    table = dynamodb.Table('monthlyReadingTable')
    resp = table.put_item(Item=item)
    print(resp)
  except Exception as e:
    print(e)

  return {
    'statusCode': 200,
    'body': json.dumps(value)
  }
