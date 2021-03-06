# Generated by Django 4.0.1 on 2022-02-01 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('meta_title', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('summary', models.TextField()),
                ('_type', models.IntegerField()),
                ('sku', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('discount', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('is_sale', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creat date')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Update date')),
                ('published_at', models.DateTimeField(null=True, verbose_name='Publish date')),
                ('starts_at', models.DateTimeField(null=True, verbose_name='start sale date')),
                ('ends_at', models.DateTimeField(null=True, verbose_name='end sale date')),
                ('content', models.TextField()),
                ('img', models.ImageField(upload_to='product/', verbose_name='Image')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_meta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('content', models.TextField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myshop.product')),
            ],
        ),
    ]
