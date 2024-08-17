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
