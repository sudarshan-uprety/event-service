import json

from apps.email_events.schema import RegisterEmail, OrderEventEmail
from apps.email_events.send_mail import register_mail, forget_password_mail, order_confirmation_mail
from utils import variables
from utils.log import logger
from utils.middleware import rabbitmq_event_handler


@rabbitmq_event_handler
def email_service_callback(ch, method, properties, body):
    body_dict = json.loads(body)

    if body_dict['event_name'] in [variables.REGISTER_EMAIL, variables.FORGET_PASSWORD_EMAIL]:
        data = RegisterEmail(**body_dict)
    elif body_dict['event_name'] == variables.ORDER_CONFIRMATION_EMAIL:
        data = OrderEventEmail(**body_dict)
    else:
        logger.error(f"Unknown event name: {body_dict['event_name']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    if data.event_name == variables.REGISTER_EMAIL:
        register_mail(to=data.to, name=data.full_name, otp=data.otp)
    elif data.event_name == variables.FORGET_PASSWORD_EMAIL:
        forget_password_mail(to=data.to, name=data.full_name, otp=data.otp)
    elif data.event_name == variables.ORDER_CONFIRMATION_EMAIL:
        order_confirmation_mail(data)
    else:
        logger.error(f"Unknown event name: {data.event_name}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
