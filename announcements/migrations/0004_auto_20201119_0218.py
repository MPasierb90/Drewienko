# Generated by Django 3.1.2 on 2020-11-19 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0003_auto_20201115_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Kategoria'),
        ),
    ]
