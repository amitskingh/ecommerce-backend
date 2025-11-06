from django.core.mail import send_mail
from django.conf import settings
from decouple import config


def my_scheduled_job():

    email = config("user_email")

    subject = "Password Reset Request"
    message = f"You're great"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)
