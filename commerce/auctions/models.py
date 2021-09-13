from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, null=True, blank=False)
    description = models.TextField(max_length=500, null=True, blank=False)
    # starting_bid = FK
    # current_bid = FK
    # winning_bid = FK
    # user_id = FK
    # winner_id = FK
    # category_id = FK
    timestamp = models.DateTimeField(auto_now_add=True)

class Bids(models.Model):
    amount = models.IntegerField(null=True, blank=False)
    # user_id = FK
    # listing_id = FK

class Watchlist(models.Model):
    # listing_id = FK
    # user_id = FK
    pass

class Comments(models.Model):
    content = models.TextField(max_length=200, null=True, blank=False)
    # user_id = FK
    # listing_id = FK

class Categories(models.Model):
    content = models.CharField(max_length=64, null=True, blank=False)

class Listings_Categories(models.Model):
    # listing_id = FK
    # category_id = FK
    pass
