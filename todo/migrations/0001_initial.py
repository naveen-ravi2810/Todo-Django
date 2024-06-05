# Generated by Django 5.0.6 on 2024-06-05 08:00

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('task', models.TextField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2024, 6, 5, 8, 0, 21, 990514))),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.users')),
            ],
        ),
    ]
