# Generated by Django 4.0.3 on 2022-04-13 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_slider_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
