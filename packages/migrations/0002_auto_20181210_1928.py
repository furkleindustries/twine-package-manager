# Generated by Django 2.1.4 on 2018-12-11 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deletedpackage',
            name='owner_id',
        ),
        migrations.AddField(
            model_name='deletedpackage',
            name='previous_owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]