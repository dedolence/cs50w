# Generated by Django 3.2.7 on 2022-01-04 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_auto_20220104_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='winning_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]