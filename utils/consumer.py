import asyncio

import aio_pika

from utils import variables
from apps.email_events.call_back import email_service_callback
from apps.lambda_events.call_back import inventory_service_callback
from apps.payment_events.call_back import payment_service_callback


async def consume_rabbitmq():
    connection = await aio_pika.connect_robust(
        f"amqp://{variables.USERNAME}:{variables.PASSWORD}@{variables.HOST}:{variables.PORT}/"
    )

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        email_queue = await channel.declare_queue(variables.EMAIL_QUEUE, durable=True)
        inventory_queue = await channel.declare_queue(variables.INVENTORY_QUEUE, durable=True)
        payment_queue = await channel.declare_queue(variables.PAYMENTS_QUEUE, durable=True)

        await email_queue.consume(email_service_callback)
        await inventory_queue.consume(inventory_service_callback)
        await payment_queue.consume(payment_service_callback)

        await asyncio.Future()

