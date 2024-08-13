import json
import uuid
import functools
from .log import logger, trace_id_var

SENSITIVE_FIELDS = ["password", "token", "api_key"]


def sanitize_payload(payload):
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return payload

    if isinstance(payload, dict):
        return {k: sanitize_payload(v) if k not in SENSITIVE_FIELDS else "******" for k, v in payload.items()}
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    else:
        return payload


def rabbitmq_event_handler(func):
    @functools.wraps(func)
    def wrapper(ch, method, properties, body):
        try:
            # Parse the message body
            message_data = json.loads(body)

            # Extract trace_id from the message or generate a new one
            trace_id = message_data.get('trace_id', str(uuid.uuid4()))
            trace_id_var.set(trace_id)

            sanitized_body = sanitize_payload(message_data)
            # logger.info(f"Received message: {method.delivery_tag}", extra={
            #     "trace_id": trace_id,
            #     "queue": method.routing_key,
            #     "body": sanitized_body
            # })

            result = func(ch, method, properties, body)

            # logger.info(f"Processed message: {method.delivery_tag}", extra={
            #     "trace_id": trace_id,
            #     "queue": method.routing_key,
            #     "result": sanitize_payload(result)
            # })

            return result
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding message {method.delivery_tag}: {str(e)}", extra={
                "trace_id": str(uuid.uuid4()),
                "queue": method.routing_key
            })
            raise
        except Exception as e:
            logger.error(f"Error processing message {method.delivery_tag}: {str(e)}", extra={
                "trace_id": trace_id_var.get(),
                "queue": method.routing_key
            })
            raise

    return wrapper
