import json

from aws_lambda import call_lambda
from schemas import InventoryProducer


def inventory_service_callback(ch, method, properties, body):
    body = json.loads(body)
    data = {
        'operation': body['operation'],
        'products': body['product']
    }
    validated_data = InventoryProducer(**data)
    call_lambda(data=validated_data.dict(), ch=ch, method=method)
