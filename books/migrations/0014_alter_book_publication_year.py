# Generated by Django 4.2.2 on 2023-07-04 18:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_alter_book_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 4, 18, 43, 46, 995131), null=True),
        ),
    ]