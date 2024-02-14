# Generated by Django 4.2.7 on 2024-02-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0005_alter_premiumowner_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premiumowner',
            name='exp_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='premiumpackages',
            name='validity',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
