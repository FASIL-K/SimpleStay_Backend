# Generated by Django 4.2.7 on 2023-12-08 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_customuser_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verify',
            field=models.BooleanField(default=False),
        ),
    ]
