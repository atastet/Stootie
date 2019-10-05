import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

DEFAULT_BODY = """
            Hi!\n 
            The Dacker Team
"""
DEFAULT_SUBJECT = 'Dacker Report'


def send_mail(body=DEFAULT_BODY, subject=DEFAULT_SUBJECT, force_mail=None):
    sender = "hello@dacker.co"
    recipients = ["pierre-francois@dacker.co", "vincent@dacker.co"]
    # zip_name = csv_path.split("/")[-1] + ".gz"
    # zip_path = csv_path + ".gz"
    # month = datetime.datetime.now().strftime("%B")
    body = MIMEText(body)
    body.set_charset('utf-8')

    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = ",".join(recipients)
    outer['From'] = sender
    outer.set_charset('utf-8')

    outer.attach(body)

    # with open(zip_path, 'rb') as fp:
    #     msg = MIMEBase("application", "octet-stream")
    #     msg.set_payload(fp.read())
    #     msg.set_charset('utf-8')
    #     msg.add_header('Content-Disposition', 'attachment; filename=' + zip_name)
    #     outer.attach(msg)

    composed = outer.as_string()
    if os.environ.get("MAIL") == "True" or force_mail:
        with smtplib.SMTP_SSL(os.environ["DACKER_EMAIL_HOST"], os.environ["DACKER_EMAIL_PORT"]) as s:
            s.login(os.environ["DACKER_EMAIL_HOST_USER"], os.environ["DACKER_EMAIL_HOST_PASSWORD"])
            s.sendmail(sender, recipients, composed)
            s.close()
