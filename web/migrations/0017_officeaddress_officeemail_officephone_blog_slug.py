# Generated by Django 4.0.3 on 2022-04-19 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_rename_discount_fk_product_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OfficeEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OfficePhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
