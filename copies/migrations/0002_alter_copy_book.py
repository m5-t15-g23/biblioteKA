# Generated by Django 4.2.2 on 2023-07-03 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_rename_user_book_users_alter_book_publication_year'),
        ('copies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='copies', to='books.book'),
        ),
    ]
