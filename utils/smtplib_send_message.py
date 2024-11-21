import smtplib
import os
import ssl
from dotenv import load_dotenv
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

passwd = os.getenv("EMAIL_PASSWD")
sender = os.getenv("EMAIL_SENDER")
receiver = os.getenv("EMAIL_RECEIVER")
context = ssl.create_default_context()


def smtp_send_html(subject, message):
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(message, 'html'))
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("mail.gmx.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(sender, passwd)
        smtp.sendmail(sender, receiver, msg.as_string())


def smtp_send_text(subject, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("mail.gmx.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(sender, passwd)
        smtp.send_message(msg)


def smtp_send_email(mail_type, subject='None', message='None'):

    with smtplib.SMTP('mail.gmx.com', port=587) as smtp:
        match mail_type:
            case 'text':
                msg = EmailMessage()
                msg.set_content(message)
            case 'html':
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(message, 'html'))
            case _:
                raise ValueError('Invalid mail_type. Expected: text or html.')

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        smtp.starttls(context=context)
        smtp.login(sender, passwd)

        # Sends txt emails
        if isinstance(msg, EmailMessage):
            smtp.send_message(msg)

        # Sends html emails
        if isinstance(msg, MIMEMultipart):
            smtp.sendmail(sender, receiver, msg.as_string())


if __name__ == "__main__":
    smtp_send_email(mail_type='text')