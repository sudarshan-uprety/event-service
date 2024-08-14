import json

from apps.email_events.schema import RegisterEmail
from apps.email_events.send_mail import register_mail, forget_password_mail
from utils import variables
from utils.log import logger
from utils.middleware import rabbitmq_event_handler


@rabbitmq_event_handler
def email_service_callback(ch, method, properties, body):
    body_dict = json.loads(body)
    data = RegisterEmail(**body_dict)

    # Log the event consumption
    logger.info(f"{{trace_id: {data.trace_id}}} Consuming email event: {data.event_name} for {data.to}", extra={
        "trace_id": data.trace_id,
        "event_name": data.event_name,
        "to": data.to,
        "full_name": data.full_name
    })

    if data.event_name == variables.REGISTER_EMAIL:
        register_mail(to=data.to, name=data.full_name, otp=data.otp)
    elif data.event_name == variables.FORGET_PASSWORD_EMAIL:
        forget_password_mail(to=data.to, name=data.full_name, otp=data.otp)
    else:
        logger.error(f"Unknown event name: {data.event_name}")

    # Log the email sending
    logger.info(f"{{trace_id: {data.trace_id}}} Email sent: {data.event_name} to {data.to}", extra={
        "trace_id": data.trace_id,
        "event_name": data.event_name,
        "to": data.to,
        "full_name": data.full_name
    })

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
