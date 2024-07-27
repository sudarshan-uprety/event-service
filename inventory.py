import json

from aws_lambda import call_lambda


def inventory_service_callback(ch, method, properties, body):
    body = json.loads(body)
    data = {
        'operation': body['operation'],
        'product': body['product'],
        'quantity': body['quantity']
    }
    call_lambda(data=data, ch=ch, method=method)
