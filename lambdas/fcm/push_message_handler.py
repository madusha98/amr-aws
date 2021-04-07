import requests
import json
from firebase_admin import messaging, credentials
import firebase_admin

def send_notification(tokens, title, body):

    if not firebase_admin._apps:
        creds = credentials.Certificate('amr-mobile-service-acc.json')
        app = firebase_admin.initialize_app(creds)

    message = messaging.MulticastMessage(tokens=tokens,
            notification=messaging.Notification(
                title=title,
                body=body,
            ),)

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)