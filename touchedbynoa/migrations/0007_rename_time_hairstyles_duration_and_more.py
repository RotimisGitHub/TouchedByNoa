# Generated by Django 4.2.7 on 2023-11-29 12:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0006_appointment_eventid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hairstyles',
            old_name='time',
            new_name='duration',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='datetime',
        ),
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.TimeField(choices=[(datetime.time(9, 0), '09:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00')], null=True),
        ),
    ]
