# Generated by Django 4.2.2 on 2023-07-07 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0023_alter_book_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 14, 15, 53, 840554), null=True),
        ),
    ]
