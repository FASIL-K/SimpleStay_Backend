# models.py
from django.db import models
from django.utils import timezone
from user.models import CustomUser
from django.core.mail import send_mail
from django.db.models.signals import post_save
# from celery import shared_task
from django.dispatch import receiver
from datetime import timedelta

class Feature(models.Model):
    name = models.CharField(max_length=100)

class PremiumPackages(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    validity = models.PositiveIntegerField(default=30)
    description = models.CharField(max_length=250)
    color = models.CharField(max_length=50)
    features = models.ManyToManyField(Feature, blank=True)


    def __str__(self):
        return self.name
    

class PremiumOwner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(PremiumPackages, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)  
    exp_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()

        self.exp_date = self.start_date + timedelta(days=self.package.validity)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'package']

@receiver(post_save, sender=PremiumOwner)
def update_user_premium_status(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.is_premium = True
        user.save()    

# @receiver(post_save, sender=PremiumOwner)
# def schedule_expiration_task(sender, instance, created, **kwargs):
#     if created:
#         # Calculate eta based on validity - 1
#         eta = instance.package.validity - 1

#         # Schedule the expiration reminder task
#         expiration_task.apply_async(
#             args=[instance.user.email, instance.package.validity],
#             countdown=eta * 24 * 60 * 60  # Convert days to seconds
            
#         )

# @shared_task()
# def expiration_task(email, validity):
#     # Send an expiration reminder (replace this with your actual message sending logic)
#     send_mail(
#         'Subscription Expiry Reminder',
#         f'Your premium subscription will expire in {validity} days.',
#         'from@example.com',
#         [email],
#         fail_silently=False,
#     )
