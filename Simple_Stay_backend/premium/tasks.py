# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from user.models import CustomUser
from datetime import timedelta
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)


   
@shared_task
def send_premium_created_email(user_email):
    logger.info(f"Sending premium created email to {user_email}")

    print(user_email,"eeeeeeeeeeeeeeeeeeeeeeeeeeee")
    # Customize your email content here
    subject = "Your premium account is successfully created"
    message = "Thank you for upgrading to premium!"
    sender_email = "simplestayinfo@gmail.com"
    
    
    # Send the email
    send_mail(subject, message, sender_email, [user_email])

@shared_task
def test_task():
    print("This is a test task. Celery is working properly!")


# # Task to send expiration reminder email
# @shared_task
# def send_expiration_reminder_email(user_email):
#     # Send expiration reminder email
#     send_mail(
#         'Subscription Expiry Reminder',
#         'Your premium subscription will expire tomorrow.',
#         'from@example.com',
#         [user_email],
#         fail_silently=False,
#     )
