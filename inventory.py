import json


def inventory_service_callback(ch, method, properties, body):
    # Process the message for the inventory service
    body = json.loads(body)
    if body['operation'] == 'reduce_product_quantity':
        product_id = body['product_id']
        product_quantity = body['product_quantity']
