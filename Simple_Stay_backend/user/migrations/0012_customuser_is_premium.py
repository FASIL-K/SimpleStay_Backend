# Generated by Django 4.2.7 on 2024-01-24 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_customuser_phone_customuser_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]
