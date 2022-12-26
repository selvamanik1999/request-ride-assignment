# Generated by Django 4.1.4 on 2022-12-24 15:18

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=1000)),
                ('destination', models.CharField(max_length=1000)),
                ('pick_up_time', models.DateTimeField()),
                ('is_flexible_time', models.BooleanField(default=False)),
                ('asset_count', models.IntegerField()),
                ('asset_type', models.CharField(choices=[('LAPTOP', 'LAPTOP'), ('TRAVEL_BAG', 'TRAVEL_BAG'), ('PACKAGE', 'PACKAGE')], max_length=1000)),
                ('sensitive', models.CharField(choices=[('HIGHLY_SENSITIVE', 'HIGHLY_SENSITIVE'), ('SENSITIVE', 'SENSITIVE'), ('NORMAL', 'NORMAL')], max_length=1000)),
                ('to_deliver_name', models.CharField(max_length=1000)),
                ('to_deliver_phone_no', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
            ],
        ),
    ]
