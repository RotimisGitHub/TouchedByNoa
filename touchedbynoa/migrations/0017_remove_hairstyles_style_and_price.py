# Generated by Django 4.2.7 on 2023-11-09 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0016_remove_appointment_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hairstyles',
            name='style_and_price',
        ),
    ]
