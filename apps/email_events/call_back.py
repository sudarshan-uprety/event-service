import json
from aio_pika import IncomingMessage

from apps.email_events.schema import RegisterEmail, OrderEventEmail
from apps.email_events.send_mail import register_mail, forget_password_mail, order_confirmation_mail
from utils import variables
from utils.log import logger
from utils.middleware import async_rabbitmq_event_handler


@async_rabbitmq_event_handler
async def email_service_callback(message: IncomingMessage):
    body_dict = json.loads(message.body.decode())

    # Process the event based on event name
    if body_dict['event_name'] in [variables.REGISTER_EMAIL, variables.FORGET_PASSWORD_EMAIL]:
        data = RegisterEmail(**body_dict)
    elif body_dict['event_name'] == variables.ORDER_CONFIRMATION_EMAIL:
        data = OrderEventEmail(**body_dict)
    else:
        logger.error(f"Unknown event name: {body_dict['event_name']}")
        return

    # Process based on event type
    if data.event_name == variables.REGISTER_EMAIL:
        await register_mail(to=data.to, name=data.full_name, otp=data.otp)
    elif data.event_name == variables.FORGET_PASSWORD_EMAIL:
        await forget_password_mail(to=data.to, name=data.full_name, otp=data.otp)
    elif data.event_name == variables.ORDER_CONFIRMATION_EMAIL:
        await order_confirmation_mail(data)
