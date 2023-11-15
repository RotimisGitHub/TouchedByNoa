# Generated by Django 4.2.7 on 2023-11-11 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0019_alter_appointment_style_and_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='style_and_price',
            field=models.TextField(choices=[('Small | £50', 'small | £50'), ('Normal | £80', 'normal | £80'), ('Large | £100', 'large | £100'), ('Extra-Large | £120', 'extra-large | £120')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(),
        ),
    ]
