# Generated by Django 4.2.7 on 2023-11-22 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_cryptocurrency_launch_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_or_photo',
            field=models.ImageField(blank=True, null=True, upload_to='id_or_photo/'),
        ),
    ]
