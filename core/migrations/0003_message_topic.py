# Generated by Django 4.2.1 on 2023-06-22 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_contact_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.CharField(default='------', max_length=200),
        ),
    ]
