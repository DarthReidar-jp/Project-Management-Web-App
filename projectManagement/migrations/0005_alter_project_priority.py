# Generated by Django 4.2.1 on 2023-06-21 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectManagement', '0004_alter_project_dead_line_alter_project_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.IntegerField(null=True),
        ),
    ]