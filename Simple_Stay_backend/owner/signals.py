from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from user.models import CustomUser



# User = get_user_model()

# @receiver(post_save, sender=CustomUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     print("signals triggerd 1")
#     try:
#         if instance.is_verify:
#             print("signals triggerd 2")
#             subject = 'Welcome to Our SimpleStay'
#             message = f'Hello {instance.email},\n\nWelcome to our website! Account was Activated Thank you for joining us.'
#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [instance.email]
#             send_mail(subject, message, from_email, recipient_list)
#     except Exception as e:
#         print(f"Exception in send_welcome_email: {e}")