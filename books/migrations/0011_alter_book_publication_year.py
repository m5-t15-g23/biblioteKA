# Generated by Django 4.2.2 on 2023-07-03 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_book_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 3, 14, 30, 23, 933699, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
