import requests
import json
from firebase_admin import messaging, credentials
import firebase_admin

def send_notification(event, context):
    # SERVER_TOKEN = 'AAAAzbJwwuU:APA91bH8O3v3S5W04FmNaXW1j5R4qySY3WtBye52hM856ikTOSf4fCnugYOah2Nq0Df9TIF6vwF4xsJJNaseNlPcyJV8h1OkOJUG3N_S1SVZk4f5oh7JGy6sAwnMJEXFIaV1nqq_0qUV'
    # DEVICE_TOKEN = 'fNeV6wnlTICE-Im2ee-N6Y:APA91bHQPHBgfwiibq7k4UN6AvHqlOIP7w031zK0tMF61W8CnpHOlrES6xwI517S2l5WSKIqxXugABe0S0dyt6acFFfjyEbESyIlVf2zpsDHskFh5EYw6MwVyqSUPNJ8pzpk8fQeAaKM'
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': 'key=' + SERVER_TOKEN,
    #   }

    # body = {
    #         'notification': {'title': 'Sending push form python script',
    #                             'body': 'New Message'
    #                             },
    #         'to':
    #             DEVICE_TOKEN,
    #         'priority': 'high',
    #         #   'data': dataPayLoad,
    #         }
    # response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    req = json.loads(event['body'])
    # registration_token = 'fNeV6wnlTICE-Im2ee-N6Y:APA91bHQPHBgfwiibq7k4UN6AvHqlOIP7w031zK0tMF61W8CnpHOlrES6xwI517S2l5WSKIqxXugABe0S0dyt6acFFfjyEbESyIlVf2zpsDHskFh5EYw6MwVyqSUPNJ8pzpk8fQeAaKM'

    creds = credentials.Certificate('amr-mobile-service-acc.json')
    app = firebase_admin.initialize_app(creds)

    # See documentation on defining a message payload.
    message = messaging.Message(
            notification=messaging.Notification(
                title='Test',
                body='Test body',
            ),
            token=req['pushToken']
        )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    return response