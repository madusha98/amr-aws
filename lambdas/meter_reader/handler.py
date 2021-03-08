import counter_recognition
import json

def read_digits(event, context):
  print('event: ')
  print(event)

  value = counter_recognition.get_reading(event)
  return {
    'statusCode': 200,
    'body': json.dumps(value)
  }
