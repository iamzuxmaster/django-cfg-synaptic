import dramatiq
from django.contrib.auth.models import User
from reset.models import UserPasswordReset
import smtplib
from core.settings import SMTP_SSL, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD
import random
import string
from core.settings import BASE_DIR
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def hasher():
    abc = ''
    for i in range(0,80):
        abc += random.choice(string.hexdigits)
    return abc

@dramatiq.actor
def send_email(email, host):
    users = User.objects.all()
    for user in users:
        if user.email == email:
            hash = hasher()
            user_reset = UserPasswordReset.objects.create(user=user, hash=hash)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Link"
            msg['From'] = SMTP_LOGIN
            msg['To'] = email
            server = smtplib.SMTP_SSL(SMTP_SSL, SMTP_PORT)
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            with open( BASE_DIR / "templates/reset/send_email.html", 'r', encoding='utf-8') as file:
                part = MIMEText(file.read(), 'html')
                msg.attach(part)
                print(file.read())
                server.sendmail(SMTP_LOGIN, email, msg.as_string().replace('[__host__]',host).replace('[__hash__]', hash))
            server.quit()