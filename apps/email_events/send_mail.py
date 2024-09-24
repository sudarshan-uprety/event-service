import aiosmtplib

from jinja2 import Environment, FileSystemLoader

from utils.variables import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT
from apps.email_events.schema import OrderEventEmail

env = Environment(loader=FileSystemLoader("apps/email_events/templates"))


async def connect_mail(retries=3):
    mail = aiosmtplib.SMTP(hostname=EMAIL_HOST, port=EMAIL_PORT, timeout=30)
    await mail.connect()
    await mail.login(EMAIL_SENDER, EMAIL_PASSWORD)
    return mail


async def send_email(subject, receivers, html_content):
    mail = await connect_mail()
    await mail.sendmail(
        EMAIL_SENDER,
        receivers,
        f"Subject: {subject}\nContent-Type: text/html\n\n{html_content}"
    )
    await mail.quit()


async def register_mail(to, otp, name):
    template = env.get_template('register_email.html')
    content = template.render(otp=otp, name=name)
    await send_email(
        subject="Verification email",
        receivers=[to],
        html_content=content
    )


async def forget_password_mail(to, otp, name):
    template = env.get_template('forget_password_email.html')
    content = template.render(otp=otp, name=name)

    await send_email(
        subject="Forget password email",
        receivers=[to],
        html_content=content
    )


async def order_confirmation_mail(data: OrderEventEmail):
    template = env.get_template('orders_email.html')

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

    await send_email(
        subject=f"Order Confirmation #{data.order_id}",
        receivers=[data.to],
        html_content=content
    )
