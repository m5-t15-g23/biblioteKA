# Generated by Django 4.2.2 on 2023-07-03 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_book_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateField(default=datetime.datetime(2023, 7, 3, 13, 47, 30, 733745, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]