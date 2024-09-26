import json

from aio_pika import IncomingMessage

from apps.lambda_events.call_lambda import call_lambda
from apps.lambda_events.schema import InventoryProducer
from utils.log import trace_id_var
from utils.middleware import async_rabbitmq_event_handler


@async_rabbitmq_event_handler
async def inventory_service_callback(message: IncomingMessage):
    body = json.loads(message.body.decode())

    # Extract or generate trace_id
    trace_id = trace_id_var.get()

    data = {
        'event_name': body['event_name'],
        'products': body['product'],
        'trace_id': trace_id
    }

    validated_data = InventoryProducer(**data)

    result = await call_lambda(data=validated_data.dict())

    return result
