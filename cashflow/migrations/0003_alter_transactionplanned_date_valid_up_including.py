# Generated by Django 4.2.7 on 2023-11-29 21:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0002_rename_name_transactioncategory_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionplanned',
            name='date_valid_up_including',
            field=models.DateField(default=datetime.datetime(2150, 12, 31, 0, 0)),
        ),
    ]
