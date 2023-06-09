# Generated by Django 4.1.6 on 2023-03-25 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Product_name',
            new_name='product_name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Seller',
            new_name='seller',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=10.0),
        ),
    ]
