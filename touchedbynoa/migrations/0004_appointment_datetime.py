# Generated by Django 4.2.7 on 2023-11-23 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0003_remove_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
