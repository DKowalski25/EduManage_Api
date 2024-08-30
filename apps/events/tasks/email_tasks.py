from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from settings import EMAIL_HOST, EMAIL_PORT, DEFAULT_FROM_EMAIL


@shared_task
def send_email_task(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = DEFAULT_FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.sendmail(DEFAULT_FROM_EMAIL, to_email, msg.as_string())


