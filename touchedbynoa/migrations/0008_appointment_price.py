# Generated by Django 4.2.7 on 2023-11-29 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0007_rename_time_hairstyles_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='price',
            field=models.PositiveIntegerField(choices=[('Small | £50', 'small | £50'), ('Normal | £80', 'normal | £80'), ('Large | £100', 'large | £100'), ('Extra-Large | £120', 'extra-large | £120')], null=True),
        ),
    ]