# Generated by Django 4.2.2 on 2023-07-03 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_publication_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='user',
            new_name='users',
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 3, 10, 28, 50, 108125), null=True),
        ),
    ]
