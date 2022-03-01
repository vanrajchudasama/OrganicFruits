# Generated by Django 4.0.1 on 2022-02-27 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myshop', '0014_product_specification_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_review',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='product_review',
            unique_together={('user_id', 'product_id')},
        ),
    ]
