# Generated by Django 4.0.3 on 2022-04-16 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_ordertypes_edit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertypes',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
