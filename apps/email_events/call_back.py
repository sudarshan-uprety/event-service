import json


def email_service_callback(ch, method, properties, body):
    # Process the message for the email service
    print('call the email service for operation')
    body = json.loads(body)
    print(body)
