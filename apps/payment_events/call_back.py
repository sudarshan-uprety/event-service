from datetime import datetime

import json

from apps.email_events.schema import OrderEventEmail, Address, ProductItem, PaymentInfo
from apps.email_events.send_mail import order_confirmation_mail


def payment_service_callback(ch, method, properties, body):
    body = json.loads(body)
    pass
    # if body['operation'] == 'payment_success':
    #     order_email = OrderEventEmail(
    #         trace_id=body['trace_id'],
    #         event_name="order_confirmation",
    #         order_id=body['order_id'],
    #         order_date=datetime.now(),
    #         to=body['customer_email'],
    #         customer_name=body['customer_name'],
    #         customer_phone=body['customer_phone'],
    #         delivery_address=Address(
    #             street=body['delivery_street'],
    #             city=body['delivery_city'],
    #             state=body['delivery_state'],
    #             zip_code=body['delivery_zip'],
    #             country=body['delivery_country']
    #         ),
    #         products=[ProductItem(**item) for item in body['items']],
    #         total_price=body['total_amount'],
    #         vendor_name=body['vendor_name'],
    #         payment_info=PaymentInfo(
    #             payment_id=body['payment_id'],
    #             payment_amount=body['payment_amount'],
    #             payment_type=body['payment_type'],
    #             payment_service=body['payment_service']
    #         ),
    #         estimated_delivery_date=body.get('estimated_delivery_date'),
    #         special_instructions=body.get('special_instructions')
    #     )
    #
    #     success = order_confirmation_mail(order_email)
    #     if success:
    #         print(f"Order confirmation email sent for order {order_email.order_id}")
    #     else:
    #         print(f"Failed to send order confirmation email for order {order_email.order_id}")

