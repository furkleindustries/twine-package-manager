# Generated by Django 2.1.3 on 2018-11-23 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('versions', '0004_auto_20181115_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='version_identifier',
            field=models.CharField(max_length=128),
        ),
    ]
