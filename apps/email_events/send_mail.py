from redmail import EmailSender

from utils.variables import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT
from utils.templates import templates


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


def order_confirmation_mail(to, order_details):
    mail = connect_mail()
    template = templates.get_template('order_email.html')

    context = {
        'order_number': order_details['order_id'],
        'items': order_details['items'],
        'total': order_details['total'],
        'payment_id': order_details['payment_id'],
        'payment_amount': order_details['payment_amount'],
        'payment_type': order_details['payment_type'],
        'payment_service': order_details['payment_service'],
    }
    content = template.render(context)

    mail.send(
        subject=f"Order Confirmation #{order_details['order_id']}",
        sender=EMAIL_SENDER,
        receivers=[to],
        html=content
    )