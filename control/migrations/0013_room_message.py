# Generated by Django 4.0.3 on 2022-05-15 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0012_remove_orderitem_order_remove_orderitem_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=250, null=True)),
                ('account_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_account_a', to='control.account')),
                ('account_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_account_b', to='control.account')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.account')),
            ],
        ),
    ]
