# Generated by Django 2.0.5 on 2018-05-24 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20180524_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='default_version',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='versions.Version'),
        ),
    ]