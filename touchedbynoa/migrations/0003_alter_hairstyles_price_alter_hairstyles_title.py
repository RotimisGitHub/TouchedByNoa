# Generated by Django 4.2.7 on 2023-11-07 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0002_appointment_client_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hairstyles',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='hairstyles',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
