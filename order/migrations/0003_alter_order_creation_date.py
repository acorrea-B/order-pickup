# Generated by Django 4.1.3 on 2022-11-10 03:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 10, 3, 40, 31, 24536, tzinfo=datetime.timezone.utc)),
        ),
    ]
