# Generated by Django 2.2.19 on 2021-08-23 22:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20210823_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(code='invalid_phone', message="Phone number must be entered in the format: '+999999999'.Up to 15 digits allowed.", regex='^\\+\\d{9,15}$')]),
        ),
    ]
