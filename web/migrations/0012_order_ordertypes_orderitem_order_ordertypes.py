# Generated by Django 4.0.3 on 2022-04-15 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_blog_img_full'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('ordertypes_comment', models.TextField(blank=True, null=True)),
                ('checkout', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.account')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=255)),
                ('priority', models.IntegerField()),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Этап заказов',
                'verbose_name_plural': 'Этап заказов',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product')),
            ],
            options={
                'verbose_name': 'Товар на Заказ',
                'verbose_name_plural': 'Товары на Заказ',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='ordertypes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.ordertypes'),
        ),
    ]
