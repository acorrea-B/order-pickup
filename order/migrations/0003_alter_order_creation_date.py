# Generated by Django 4.1.3 on 2022-11-09 21:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_creation_date_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 9, 21, 47, 39, 196346, tzinfo=datetime.timezone.utc)),
        ),
    ]
