# Generated by Django 4.2.7 on 2023-11-20 15:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_delete_crypto_news_published_date_user_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='launch_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
