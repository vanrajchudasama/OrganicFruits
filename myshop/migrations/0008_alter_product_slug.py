# Generated by Django 4.0.1 on 2022-02-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0007_alter_product_review_product_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
