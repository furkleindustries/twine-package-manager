# Generated by Django 2.0.5 on 2018-05-24 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_email_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='homepage',
            field=models.URLField(blank=True, default=''),
        ),
    ]