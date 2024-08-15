import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError

from utils.variables import HOST, USERNAME, PASSWORD, PORT, EMAIL_QUEUE, INVENTORY_QUEUE, PAYMENTS_QUEUE
from apps.email_events.call_back import email_service_callback
from apps.lambda_events.call_back import inventory_service_callback
from apps.payment_events.call_back import payment_service_callback


def connect_rabbit():
    try:
        credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials))
        channel = connection.channel()

        # Declare the queues for email and inventory services
        channel.queue_declare(queue=EMAIL_QUEUE, durable=True)
        channel.queue_declare(queue=INVENTORY_QUEUE, durable=True)
        channel.queue_declare(queue=PAYMENTS_QUEUE, durable=True)

        # Set prefetch count for fair dispatch
        channel.basic_qos(prefetch_count=2)

        # Start consuming messages from email_events queue
        channel.basic_consume(queue=EMAIL_QUEUE, on_message_callback=email_service_callback, auto_ack=False)

        # Start consuming messages from inventory_events queue
        channel.basic_consume(queue=INVENTORY_QUEUE, on_message_callback=inventory_service_callback, auto_ack=False)

        # Start consuming messages from payment_event queue
        channel.basic_consume(queue=PAYMENTS_QUEUE, on_message_callback=payment_service_callback, auto_ack=False)

        print("Started consuming events...")
        channel.start_consuming()
    except AMQPConnectionError as e:
        print(f"Connection error: {e}")
    except AMQPChannelError as e:
        print(f"Channel error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    connect_rabbit()
