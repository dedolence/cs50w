# Generated by Django 3.2.7 on 2022-01-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_auto_20211230_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='autodelete',
            field=models.BooleanField(default=False, help_text='True indicates the notification should be deleted as soon as it is rendered.'),
        ),
    ]
