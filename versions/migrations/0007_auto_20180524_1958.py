# Generated by Django 2.0.5 on 2018-05-24 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('versions', '0006_auto_20180524_1956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='version',
            old_name='created_time',
            new_name='date_created',
        ),
    ]