# Generated by Django 4.2.7 on 2023-11-14 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touchedbynoa', '0026_rename_name_appointment_title_alter_hairstyles_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='style_and_price',
        ),
        migrations.AddField(
            model_name='appointment',
            name='size',
            field=models.CharField(choices=[('Small', 'small'), ('Normal | £80', 'normal'), ('Large', 'large'), ('Extra-Large', 'extra-large')], max_length=100, null=True),
        ),
    ]
