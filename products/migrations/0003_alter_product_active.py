# Generated by Django 5.1.4 on 2024-12-22 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_productfeature_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(),
        ),
    ]
