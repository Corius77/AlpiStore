# Generated by Django 4.2.1 on 2023-06-23 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_remove_orderitem_sizes_orderitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]