# Generated by Django 4.0.1 on 2022-01-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_customuser_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile',
            field=models.BigIntegerField(blank=True, unique=True),
        ),
    ]
