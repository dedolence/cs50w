# Generated by Django 3.2.7 on 2021-12-30 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_notifications'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notifications',
            new_name='Notification',
        ),
    ]
