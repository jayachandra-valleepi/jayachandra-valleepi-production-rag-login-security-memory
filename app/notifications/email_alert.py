from flask_mail import Mail
from flask_mail import Message


mail = Mail()


def send_security_alert(email):

    msg = Message(
        subject="Security Alert",
        sender="example@gmail.com",
        recipients=[email]
    )

    msg.body = "Someone logged into your account."

    mail.send(msg)