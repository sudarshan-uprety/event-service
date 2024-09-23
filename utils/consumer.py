import asyncio
import aio_pika
from utils import variables
from utils.log import logger

from apps.email_events.call_back import email_service_callback
from apps.lambda_events.call_back import inventory_service_callback
from apps.payment_events.call_back import payment_service_callback


async def consume_rabbitmq():
    try:
        connection = await aio_pika.connect_robust(
            f"amqp://{variables.USERNAME}:{variables.PASSWORD}@{variables.HOST}:{variables.PORT}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            email_queue = await channel.declare_queue(variables.EMAIL_QUEUE, durable=True)
            inventory_queue = await channel.declare_queue(variables.INVENTORY_QUEUE, durable=True)
            payment_queue = await channel.declare_queue(variables.PAYMENTS_QUEUE, durable=True)

            consumer_tasks = [
                asyncio.create_task(email_queue.consume(email_service_callback)),
                asyncio.create_task(inventory_queue.consume(inventory_service_callback)),
                asyncio.create_task(payment_queue.consume(payment_service_callback))
            ]

            try:
                await asyncio.gather(*consumer_tasks)
            except asyncio.CancelledError:
                print('heee')
                logger.info("Consumer tasks are being cancelled...")
                for task in consumer_tasks:
                    task.cancel()
                await asyncio.gather(*consumer_tasks, return_exceptions=True)
                logger.info("All consumer tasks have been cancelled.")
            finally:
                await connection.close()

    except aio_pika.AMQPException as e:
        print('heee', e)
        logger.error(f"AMQP Error: {e}")
    except Exception as e:
        print('heeeheee', e)
        logger.error(f"Unexpected error in consume_rabbitmq: {e}")

# Your callback functions (email_service_callback, etc.) go here