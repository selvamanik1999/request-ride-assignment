# Generated by Django 4.1.4 on 2022-12-24 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride_api', '0003_requester_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requester',
            name='status',
        ),
    ]
