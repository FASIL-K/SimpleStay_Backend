# Generated by Django 4.2.7 on 2024-01-24 18:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('premium', '0003_feature_remove_premiumpackages_features_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='premiumowner',
            unique_together={('user', 'package')},
        ),
    ]