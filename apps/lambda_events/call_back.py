import json

from apps.lambda_events.call_lambda import call_lambda
from apps.lambda_events.schema import InventoryProducer
from utils.log import trace_id_var
from utils.middleware import async_rabbitmq_event_handler
import uuid


@async_rabbitmq_event_handler
def inventory_service_callback(ch, method, properties, body):
    body = json.loads(body)

    # Extract or generate trace_id
    trace_id = trace_id_var.get()

    data = {
        'event_name': body['event_name'],
        'products': body['product'],
        'trace_id': trace_id
    }

    validated_data = InventoryProducer(**data)

    result = call_lambda(data=validated_data.dict(), ch=ch, method=method)

    return result
