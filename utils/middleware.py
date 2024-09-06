import json
import uuid
import functools
import time  # For tracking process time

from .log import logger, trace_id_var

SENSITIVE_FIELDS = ["password", "confirm_password", "token", "api_key"]


def rabbitmq_event_handler(func):
    @functools.wraps(func)
    def wrapper(ch, method, properties, body):
        # accessing this variable outside of try catch because to pass it to logger even if the exception occurred.
        start_time = time.time()
        trace_id = str(uuid.uuid4())
        message_data = json.loads(body)
        try:
            trace_id = message_data.get('trace_id', trace_id)
            trace_id_var.set(trace_id)

            result = func(ch, method, properties, body)

            # Calculate the total processing time
            process_time = time.time() - start_time

            # Log the successful event consumption
            log_data = {
                "trace_id": trace_id,
                "process_time": f"{process_time:.4f}",  # Process time in seconds (up to 4 decimals)
                "event_name": message_data.get("event_name"),
                "status_code": 200
            }

            # Log success with status code 200
            logger.info(f"Request completed successfully: {json.dumps(log_data)}", extra={
                "trace_id": trace_id
            })

            return result

        except json.JSONDecodeError as e:
            # Log the error with a 400 status code (Bad Request for malformed JSON)
            process_time = time.time() - start_time
            log_error(method, trace_id, process_time, 400, f"Error decoding message: {str(e)}", )
            raise
        except Exception as e:
            # Log the error with a 500 status code (Internal Server Error)
            process_time = time.time() - start_time
            log_error(
                trace_id=trace_id_var.get(),
                process_time=process_time,
                status_code=500,
                error_message=f"Error processing message: {str(e)}",
                event_name=message_data.get("event_name")
            )
            raise

    return wrapper


def log_error(trace_id, process_time, status_code, error_message, event_name):
    """Helper function to log errors in the same format as success logs."""
    log_data = {
        "trace_id": trace_id,
        "process_time": f"{process_time:.4f}" if process_time else "N/A",
        "event_name": event_name,
        "status_code": status_code,
        "error": error_message
    }

    logger.error(f"Request failed: {json.dumps(log_data)}", extra={
        "trace_id": trace_id
    })
