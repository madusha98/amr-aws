import requests
import json

def send_notification(event, context):
    SERVER_TOKEN = 'AAAAzbJwwuU:APA91bH8O3v3S5W04FmNaXW1j5R4qySY3WtBye52hM856ikTOSf4fCnugYOah2Nq0Df9TIF6vwF4xsJJNaseNlPcyJV8h1OkOJUG3N_S1SVZk4f5oh7JGy6sAwnMJEXFIaV1nqq_0qUV'
    DEVICE_TOKEN = 'fNeV6wnlTICE-Im2ee-N6Y:APA91bHQPHBgfwiibq7k4UN6AvHqlOIP7w031zK0tMF61W8CnpHOlrES6xwI517S2l5WSKIqxXugABe0S0dyt6acFFfjyEbESyIlVf2zpsDHskFh5EYw6MwVyqSUPNJ8pzpk8fQeAaKM'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + SERVER_TOKEN,
      }

    body = {
            'notification': {'title': 'Sending push form python script',
                                'body': 'New Message'
                                },
            'to':
                DEVICE_TOKEN,
            'priority': 'high',
            #   'data': dataPayLoad,
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

    return response