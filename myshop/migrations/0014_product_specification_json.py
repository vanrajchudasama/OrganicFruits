# Generated by Django 4.0.1 on 2022-02-26 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0013_product_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='specification_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]