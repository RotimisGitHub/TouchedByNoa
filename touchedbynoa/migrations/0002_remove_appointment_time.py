# Generated by Django 4.2.7 on 2023-11-23 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
    ]