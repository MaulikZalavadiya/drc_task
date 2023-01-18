import re
from django.core.mail import send_mail
import random
from django.conf import settings
# from .models import User
from custom_auth.models import User


def send_otp(email,otp):
    subject="Your account varification email "
    message=f'Your otp is {otp}'
    email_from=settings.EMAIL_HOST_USER

    try:
        print('before>>>>>>>>>')
        send_mail(subject,message,email_from,[email])
        return True
    except Exception as e:
        print(e, 'send otp msg')
        return False