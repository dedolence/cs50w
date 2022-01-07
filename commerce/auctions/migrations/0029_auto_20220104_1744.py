# Generated by Django 3.2.7 on 2022-01-04 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_auto_20220103_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(related_name='users_watchlist', to='auctions.Listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users_listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FAKE_RELATED_NAME_FOR_LISTING_FIELD', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FAKE_RELATED_NAME_FOR_USER_FIELD', to=settings.AUTH_USER_MODEL),
        ),
    ]
