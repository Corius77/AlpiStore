# Generated by Django 4.2.1 on 2023-06-23 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_delivery_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='sizes',
            field=models.ManyToManyField(to='product.size'),
        ),
    ]