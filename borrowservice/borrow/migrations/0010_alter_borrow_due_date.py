# Generated by Django 5.0.3 on 2024-04-05 07:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0009_alter_borrow_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 12, 7, 3, 9, 371985, tzinfo=datetime.timezone.utc)),
        ),
    ]