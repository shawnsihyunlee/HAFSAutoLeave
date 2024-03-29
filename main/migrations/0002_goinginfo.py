# Generated by Django 2.2.3 on 2019-08-02 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoingInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('do_auto_signup', models.BooleanField(default=False)),
                ('out_day', models.CharField(max_length=10)),
                ('out_hour', models.IntegerField()),
                ('out_minute', models.IntegerField()),
                ('return_day', models.CharField(max_length=10)),
                ('return_hour', models.IntegerField()),
                ('return_minute', models.IntegerField()),
            ],
        ),
    ]
