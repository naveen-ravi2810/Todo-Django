# Generated by Django 5.0.6 on 2024-06-06 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todos_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='todos',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]