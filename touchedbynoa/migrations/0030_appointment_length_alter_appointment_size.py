# Generated by Django 4.2.7 on 2023-11-14 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0029_alter_appointment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='length',
            field=models.CharField(choices=[('Bra', 'bra'), ('Mid-Back', 'mid-back'), ('Waist', 'waist'), ('Butt', 'butt'), ('Mid Thighs', 'mid thighs'), ('Knees', 'knees')], default='Mid-Back', max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='size',
            field=models.CharField(choices=[('Small', 'small'), ('Normal', 'normal'), ('Large', 'large'), ('Extra-Large', 'extra-large')], default='Normal', max_length=100),
        ),
    ]
