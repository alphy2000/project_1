# Generated by Django 4.2.7 on 2023-11-28 13:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='category',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
