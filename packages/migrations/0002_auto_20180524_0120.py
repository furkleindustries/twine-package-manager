# Generated by Django 2.0.5 on 2018-05-24 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='package',
            name='homepage',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='package',
            name='keywords',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='package',
            name='tag',
            field=models.TextField(blank=True, default=''),
        ),
    ]
