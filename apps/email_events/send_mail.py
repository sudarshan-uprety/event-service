from redmail import gmail

from utils.variables import EMAIL_SENDER, EMAIL_PASSWORD
from utils.templates import templates


def connect_mail():
    gmail.username = EMAIL_SENDER
    gmail.password = EMAIL_PASSWORD
    return gmail


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
    template = templates.get_template('forget_password_mail.html')
    content = template.render(otp=otp, name=name)

    mail.send(
        subject="Forget password email",
        sender=EMAIL_SENDER,
        receivers=[to],
        html=content
    )
