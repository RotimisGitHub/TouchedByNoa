# Generated by Django 4.2.7 on 2023-12-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0011_remove_appointment_payment_bool_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='eventID',
            new_name='calendar_event_id',
        ),
        migrations.AddField(
            model_name='appointment',
            name='stripe_checkout_id',
            field=models.CharField(max_length=500, null=True),
        ),
    ]