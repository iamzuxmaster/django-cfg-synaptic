# Generated by Django 4.0.3 on 2022-04-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_order_ordertypes_orderitem_order_ordertypes'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='drop',
            field=models.BooleanField(default=False),
        ),
    ]
