import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError

from variables import HOST, USERNAME, PASSWORD, PORT
from email_service import email_service_callback
from inventory import inventory_service_callback
from payment import payment_service_callback


def connect_rabbit():
    try:
        credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials))
        channel = connection.channel()

        # Declare the queues for email and inventory services
        channel.queue_declare(queue='email_events', durable=True)
        channel.queue_declare(queue='inventory_events', durable=True)
        channel.queue_declare(queue='payment_events', durable=True)

        # Set prefetch count for fair dispatch
        channel.basic_qos(prefetch_count=2)

        # Start consuming messages from email_events queue
        channel.basic_consume(queue='email_events', on_message_callback=email_service_callback, auto_ack=False)

        # Start consuming messages from inventory_events queue
        channel.basic_consume(queue='inventory_events', on_message_callback=inventory_service_callback, auto_ack=False)

        # Start consuming messages from payment_event queue
        channel.basic_consume(queue='payment_events', on_message_callback=payment_service_callback, auto_ack=False)

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
