# Generated by Django 4.2.7 on 2024-01-19 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_customuser_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='profile_photo',
        ),
    ]