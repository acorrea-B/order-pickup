# Generated by Django 4.1.3 on 2022-11-10 03:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 10, 3, 36, 1, 976456, tzinfo=datetime.timezone.utc)),
        ),
    ]
