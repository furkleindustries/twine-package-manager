# Generated by Django 2.0.5 on 2018-11-14 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='')),
                ('homepage', models.URLField(blank=True, default='')),
                ('email_visible', models.BooleanField(default=False)),
                ('date_style', models.CharField(choices=[('DDMM', 'Day first'), ('MMDD', 'Month first')], default='MMDD', max_length=4)),
                ('time_style', models.CharField(choices=[('12H', 'Twelve hours'), ('24H', 'Twenty-four hours')], default='12H', max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
