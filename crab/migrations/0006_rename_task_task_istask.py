# Generated by Django 4.0.3 on 2022-05-06 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crab', '0005_task_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task',
            new_name='istask',
        ),
    ]