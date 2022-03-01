# Generated by Django 4.0.1 on 2022-02-17 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myshop', '0010_tag_product_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('new', 'New'), ('cart', 'Cart'), ('checkout', 'Checkout'), ('paid', 'Paid'), ('complete', 'Complete'), ('abandoned', 'Abandoned')], max_length=15)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=100)),
                ('line1', models.CharField(max_length=50)),
                ('line2', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creat date')),
                ('updatedAt', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Update date')),
                ('content', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
