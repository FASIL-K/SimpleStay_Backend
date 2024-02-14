# tasks.py
from celery import shared_task
from django.core.mail import send_mail,BadHeaderError
from user.models import CustomUser
from datetime import timedelta
from django.utils import timezone
import logging
from .models import PremiumOwner
from django.http import HttpResponse

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


# @shared_task
# def check_package_expiration():
#     logger.info("Checking package expiration")

#     # Get all premium owners whose expiration date is within one day
#     expiring_packages = PremiumOwner.objects.filter(
#         exp_date=timezone.now().date() + timedelta(days=1)
#     )

#     for package in expiring_packages:
#         user_email = package.user.email
#         logger.info(f"Sending expiration notification to {user_email}")

#         # Customize your email content here
#         subject = "Your premium subscription is expiring soon"
#         message = "Your premium subscription is expiring tomorrow. Please renew your subscription to continue enjoying premium benefits."
#         sender_email = "simplestayinfo@gmail.com"

#         # Send the email
#         send_mail(subject, message, sender_email, [user_email])

#     # Get all premium owners whose expiration date has passed
#     expired_packages = PremiumOwner.objects.filter(exp_date__lt=timezone.now().date())

#     for package in expired_packages:
#         logger.info(f"Package for user {package.user.email} has expired")
#         # Update the is_premium field of the user model to False
#         package.user.is_premium = False
#         package.user.save()


@shared_task
def check_package_expiration():
    logger.info("Checking package expiration")

    # Get all premium owners whose expiration date is within one minute
    expiring_packages = PremiumOwner.objects.filter(
        exp_date__gt=timezone.now() - timedelta(days=1),
        exp_date__lte=timezone.now()  # Expires now or in the past
    )


    for package in expiring_packages:
        user_email = package.user.email
        logger.info(package,"eeeeeeeeeeeeeeeeeeeeeeeeeee")
        logger.info(f"Sending expiration notification to {user_email}")

        # Customize your email content here
        send_expiration_reminder_email.delay(user_email)
    # Get all premium owners whose expiration date has passed
    expired_packages = PremiumOwner.objects.filter(exp_date__lt=timezone.now())
    print(expired_packages,"expirrrrrrrrrrrrrrr")
    logger.info(expired_packages,"dasdasdas")
    for package in expired_packages:
        logger.info(f"Package for user {package.user.email} has expired")
        # Check if the user's premium status is already False before updating
        if package.user.is_premium  :
            # Update the is_premium field of the user model to False
            package.user.is_premium = False
            package.is_active = False  # Assuming this is the package's active status
            send_expiration_reminder_email.delay(package.user.email) 

            package.user.save()
            package.save()

# # Task to send expiration reminder email
@shared_task
def send_expiration_reminder_email(user_email):
    # Send expiration reminder email
    send_mail(
        'Subscription Expiry Reminder',
        'Your premium subscription will expired.',
        'simplestayinfo@gmail.com',
        [user_email],
        fail_silently=False,
    )
