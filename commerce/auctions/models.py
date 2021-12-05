from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.expressions import F


class User(AbstractUser):
    Comment = models.ManyToManyField('Comment', blank=True)

class Listing(models.Model):
    image_url = models.CharField(max_length=200, null=True, blank=False)
    title = models.CharField(max_length=64, null=True, blank=False)
    description = models.TextField(max_length=500, null=True, blank=False)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    shipping = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=PROTECT, related_name='listings', null=True)
    winner = models.ForeignKey(User, on_delete=PROTECT, related_name='won_listings', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=CASCADE, related_name='category_listings', null=True, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Listing title: {self.title}. Owner: {self.user_id}. Starting bid: {self.starting_bid}. Created at {self.timestamp}."

class Bid(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=PROTECT, null=True)
    listing = models.ForeignKey(Listing, on_delete=CASCADE, null=True)

    def __str__(self):
        return f"Amount: {self.amount} by {self.user_id}"

class Comment(models.Model):
    content = models.TextField(max_length=200, null=True, blank=False)

class Category(models.Model):
    content = models.CharField(max_length=64, null=True, blank=False)

    def __str__(self):
        return f"Category: {self.content}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name='being_watched_by')

    def __str__(self):
        return f"Watching: {self.listing}"