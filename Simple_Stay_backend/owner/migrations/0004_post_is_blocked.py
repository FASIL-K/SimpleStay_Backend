# Generated by Django 4.2.7 on 2024-01-02 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0003_post_is_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
