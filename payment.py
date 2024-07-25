import json


def payment_service_callback(ch, method, properties, body):
    # Process the message for the payment service
    body = json.loads(body)
    if body['operation'] == 'payment_success':
        payment_id = body['payment_id']
        payment_amount = body['payment_amount']
        payment_type = body['payment_type']
        payment_service = body['payment_service']
        order_id = body['order_id']
        product_id = body['product_id']
