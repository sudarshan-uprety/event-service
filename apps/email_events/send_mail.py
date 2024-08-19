from redmail import EmailSender

from utils.variables import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT
from utils.templates import templates
from apps.email_events.schema import OrderEventEmail


def connect_mail():
    try:
        mail = EmailSender(
            host=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_SENDER,
            password=EMAIL_PASSWORD,

        )
        return mail
    except Exception as e:
        print(e)


def register_mail(to, otp, name):
    mail = connect_mail()
    template = templates.get_template('register_email.html')
    content = template.render(otp=otp, name=name)

    mail.send(
        subject="Verification email",
        sender=EMAIL_SENDER,
        receivers=[to],
        html=content
    )


def forget_password_mail(to, otp, name):
    mail = connect_mail()
    template = templates.get_template('forget_password_email.html')
    content = template.render(otp=otp, name=name)

    mail.send(
        subject="Forget password email",
        sender=EMAIL_SENDER,
        receivers=[to],
        html=content
    )


def order_confirmation_mail(data: OrderEventEmail):
    mail = connect_mail()
    template = templates.get_template('orders_email.html')

    context = {
        'order_number': data.order_id,
        'customer_name': data.full_name,
        'customer_email': data.to,
        'customer_phone': data.customer_phone,
        'delivery_address': {
            'street': data.delivery_address,
            'city': '',
            'state': '',
            'zip_code': '',
            'country': ''
        },
        'items': [
            {
                'name': item.name,
                'quantity': item.quantity,
                'price_per_item': item.price,
                'total': item.total
            } for item in data.products
        ],
        'total': data.total_price,
        'payment_id': data.payment_id,
        'payment_amount': data.payment_amount,
        'payment_type': data.payment_method,
    }
    content = template.render(context)

    mail.send(
        subject=f"Order Confirmation #{data.order_id}",
        sender=EMAIL_SENDER,
        receivers=[data.to],
        html=content
    )
