# Generated by Django 4.2.1 on 2023-07-15 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectManagement', '0004_task_task_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_member',
        ),
    ]
