# Generated by Django 4.0.3 on 2022-04-25 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_office_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]