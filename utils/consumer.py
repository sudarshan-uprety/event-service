import aio_pika
import asyncio

from utils.variables import HOST, USERNAME, PASSWORD, PORT, EMAIL_QUEUE, INVENTORY_QUEUE, PAYMENTS_QUEUE
from apps.email_events.call_back import email_service_callback
from apps.lambda_events.call_back import inventory_service_callback
from apps.payment_events.call_back import payment_service_callback


async def consume_rabbitmq():
    connection = await aio_pika.connect_robust(
        f"amqp://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/"
    )

    async with connection:
        channel = await connection.channel()

        # Set prefetch count
        await channel.set_qos(prefetch_count=1)

        # Declare queues
        email_queue = await channel.declare_queue(EMAIL_QUEUE, durable=True)
        inventory_queue = await channel.declare_queue(INVENTORY_QUEUE, durable=True)
        payment_queue = await channel.declare_queue(PAYMENTS_QUEUE, durable=True)

        # Consume messages
        await email_queue.consume(email_service_callback)
        await inventory_queue.consume(inventory_service_callback)
        await payment_queue.consume(payment_service_callback)

        await asyncio.Future()
