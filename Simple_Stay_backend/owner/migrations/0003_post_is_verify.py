# Generated by Django 4.2.7 on 2024-01-01 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0002_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_verify',
            field=models.BooleanField(default=False),
        ),
    ]
