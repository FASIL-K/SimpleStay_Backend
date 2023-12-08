# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.db import models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verification_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_verification_email_async(instance)

def send_verification_email_async(user):
    current_site = get_current_site()
    mail_subject = 'Please activate your account'
    message = render_to_string('user/account_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=message,
    )

def get_current_site():
    # Customize this method based on your project's URL configuration
    return 'example.com'  # Replace with your actual domain
