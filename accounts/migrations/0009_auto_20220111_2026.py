# Generated by Django 3.1.13 on 2022-01-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customuser_is_varified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='auth_token',
            field=models.CharField(editable=False, max_length=150),
        ),
    ]
