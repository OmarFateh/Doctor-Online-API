# Generated by Django 2.2.19 on 2021-08-23 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='birthdate',
            field=models.DateField(null=True),
        ),
    ]
