# Generated by Django 2.0.3 on 2019-07-28 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='product',
            new_name='product_slug',
        ),
    ]
