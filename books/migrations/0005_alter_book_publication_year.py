# Generated by Django 4.2.2 on 2023-07-01 23:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 1, 20, 43, 2, 356958), null=True),
        ),
    ]