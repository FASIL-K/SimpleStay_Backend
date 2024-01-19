# Generated by Django 4.2.7 on 2024-01-19 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_remove_customuser_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.FileField(blank=True, null=True, upload_to='Userprofiles/'),
        ),
    ]
