# Generated by Django 4.0.3 on 2022-05-06 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0012_remove_orderitem_order_remove_orderitem_product_and_more'),
        ('crab', '0008_alter_order_options_order_date_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='control.product'),
        ),
    ]
