# Generated by Django 4.2.2 on 2023-07-01 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('copies', '0001_initial'),
        ('loans', '0003_rename_copie_loan_copy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='copy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan', to='copies.copy'),
        ),
    ]
