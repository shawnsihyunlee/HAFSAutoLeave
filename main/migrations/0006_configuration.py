# Generated by Django 2.2.4 on 2019-10-12 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_goinginfo_leave_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_auto_signup', models.BooleanField(default=True)),
            ],
        ),
    ]