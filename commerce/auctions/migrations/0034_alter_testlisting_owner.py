# Generated by Django 3.2.7 on 2022-01-05 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_auto_20220105_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testlisting',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='auctions.testuser'),
        ),
    ]