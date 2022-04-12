# Generated by Django 4.0.3 on 2022-04-12 16:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('role', models.CharField(choices=[('client', 'Client'), ('moderator', 'Moderator-Admin'), ('admin', 'Controller'), ('superadmin', 'SuperAdmin')], max_length=255)),
                ('telegram_id', models.IntegerField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=250)),
                ('priority', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('unit', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('title_ru', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('description_ru', models.TextField()),
                ('slug', models.CharField(max_length=255)),
                ('priority', models.IntegerField()),
                ('price', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('drop', models.BooleanField(default=False)),
                ('img_min', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[300, 300], upload_to='web/products/300x300/')),
                ('img_full', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[600, 600], upload_to='web/products/600x600/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.category')),
                ('discount_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.discount')),
            ],
            options={
                'verbose_name': 'Наименование',
                'verbose_name_plural': 'Наименовании',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('img_min', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, size=[300, 300], upload_to='web/sliders/700x300/')),
                ('img_full', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=100, size=[1200, 500], upload_to='web/sliders/1200x500/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайды',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('priority', models.IntegerField()),
                ('slug', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.category')),
            ],
            options={
                'verbose_name': 'ПодКатегория',
                'verbose_name_plural': 'ПодКатегории',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_min', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[300, 300], upload_to='web/products/300x300/')),
                ('img_full', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=100, size=[600, 600], upload_to='web/products/600x600/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product')),
            ],
            options={
                'verbose_name': 'Фото продукт',
                'verbose_name_plural': 'Фото продукты',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.subcategory'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.country')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Городы',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.account')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блог',
            },
        ),
    ]