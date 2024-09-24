import json
import uuid
import time
from functools import wraps
from typing import Callable

from fastapi import Request, Response
from aio_pika import IncomingMessage

from utils.log import logger, set_trace_id, trace_id_var

# List of sensitive fields to redact
SENSITIVE_FIELDS = [
    "password", "confirm_password", "new_password", "current_password",
    "access_token", "refresh_token", "otp", "code"
]


def sanitize_payload(payload):
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return payload

    if isinstance(payload, dict):
        return {k: "******" if k in SENSITIVE_FIELDS else sanitize_payload(v) for k, v in payload.items()}
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    return payload


async def optimized_logging_middleware(request: Request, call_next: Callable) -> Response:
    trace_id = request.headers.get("X-Trace-ID")
    trace_id = set_trace_id(trace_id)  # This will create a new trace_id if none was provided

    start_time = time.time()
    client_ip = request.client.host

    # Get and redact the request body
    try:
        request_body = await request.json()
    except json.JSONDecodeError:
        request_body = (await request.body()).decode() or ""

    sanitized_body = sanitize_payload(request_body)

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "trace_id": trace_id,
        "client_ip": client_ip,
        "request_payload": sanitized_body
    }

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        status_code = response.status_code

        log_dict.update({
            "process_time": f"{process_time:.4f}",
            "status_code": status_code
        })

        log_message = json.dumps(log_dict)

        if status_code >= 500:
            logger.error(f"Request failed: {log_message}")
        elif status_code >= 400:
            logger.warning(f"Request resulted in client error: {log_message}")
        else:
            logger.info(f"Request completed successfully: {log_message}")

        return response

    except Exception as e:
        # Log the exception and re-raise it to be handled by global exception handlers
        logger.exception("Unhandled exception during request processing", extra=log_dict)
        raise e


def async_rabbitmq_event_handler(func):
    @wraps(func)
    async def wrapper(message: IncomingMessage):
        start_time = time.time()
        trace_id = str(uuid.uuid4())

        async with message.process():
            try:
                body = message.body.decode()
                message_data = json.loads(body)
                trace_id = message_data.get('trace_id', trace_id)
                trace_id_var.set(trace_id)

                await func(message)

                process_time = time.time() - start_time

                log_data = {
                    "trace_id": trace_id,
                    "process_time": f"{process_time:.4f}",
                    "event_name": message_data.get("event_name"),
                    "status_code": 200
                }

                logger.info(f"Event processed successfully: {json.dumps(log_data)}", extra={"trace_id": trace_id})

            except json.JSONDecodeError as e:
                process_time = time.time() - start_time
                log_error(trace_id, process_time, 400, f"Error decoding message: {str(e)}",
                          message_data.get("event_name"))
            except Exception as e:
                process_time = time.time() - start_time
                log_error(trace_id, process_time, 500, f"Error processing message: {str(e)}",
                          message_data.get("event_name"))
                raise

    return wrapper


def log_error(trace_id, process_time, status_code, error_message, event_name):
    log_data = {
        "trace_id": trace_id,
        "process_time": f"{process_time:.4f}" if process_time else "N/A",
        "event_name": event_name,
        "status_code": status_code,
        "error": error_message
    }

    logger.error(f"Event processing failed: {json.dumps(log_data)}", extra={"trace_id": trace_id})
