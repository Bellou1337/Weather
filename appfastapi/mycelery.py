from celery import Celery

import smtplib
from email.message import EmailMessage


# celery -A mycelery worker -P solo -l info
# celery -A mycelery flower

app = Celery('mycelery', broker='redis://redis:6379/0')
app.conf.broker_connection_retry_on_startup = True

@app.task(name='mycelery.send_text_mail_task')
def send_text_mail_task(server, port, email, password, to_email, subject, text_message):
    with smtplib.SMTP(server, port) as mail_server:
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(email, password)

        mail_server.sendmail(email, to_email, f"Subject: {subject}\n\n{text_message}".encode('utf-8'))

@app.task(name='mycelery.send_HTML_mail_task')
def send_HTML_mail_task(server, port, email, password, to_email, subject, html):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to_email
    msg.add_header('Content-Type','text/html')
    msg.set_payload(html)

    with smtplib.SMTP(server, port) as mail_server:
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(email, password)

        mail_server.sendmail(email, to_email, msg.as_string().encode('utf-8'))
        
        
