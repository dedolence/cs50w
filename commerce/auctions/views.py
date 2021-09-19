from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import get_template

from .models import User, Listing, Bid, Comment, Category, Watchlist

#for testing
from . import wordlist
import random
import urllib.request
from essential_generators import DocumentGenerator
gen = DocumentGenerator()

def index(request):
    active_listings = Listing.objects.filter(user_id=request.user.id)
    
    return render(request, "auctions/index.html", {
        'active_listings': active_listings,
        'watchlist': getWatchlist(request.user.id)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return render(request, "auctions/index.html", {
        "message": "You have been logged out."
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listings(request):
    return render(request, "auctions/listings.html", {
        "listings": Listing.objects.all()
    })

def listing_page(request, listing_id):
    return render(request, "auctions/listing.html", {
        'listing': Listing.objects.get(pk=listing_id)
    })

def create_listing(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/createListing.html")

def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })

def category(request, category):
    category_listings = Category.objects.filter(content__iexact=category)       # content is the column, __iexact is a case-insensitive LIKE query
    return render(request, "auctions/category.html", {
        "category_listings": category_listings
    })


def getWatchlist(user_id):
    """
        Gets a user's watchlist based on their ID.
        For a plain descriptive string of the listing being watched, one could simply
        get a queryset from the join table itself, which Django nicely cross-references
        to fill in the details. But this doesn't return an object with accessible
        properties like listing.title, or listing.description; hence, separate DB queries.
    """
    watch_joinset = Watchlist.objects.filter(user_id=user_id)
    watchlist = []
    for watch_item in watch_joinset:
        watchlist.append(Listing.objects.get(pk=watch_item.listing_id))

    return watchlist

def view_user(request, username):
    return render(request, "auctions/user.html", {
        "user": username
    })

# testing methods below
def viewMockup(request):
    titles = generateListing(10)
    return render(request, "auctions/mockup.html", {
        "titles": titles
    })


def generateListing(amount):
    listings = []
    for i in range(amount):
        listing = {}

        listing['title'] = generateTitle()
        listing['image_path'] = generateImage(i)
        listing['description'] = generateDescription()
        listing['price'] = random.randint(1,9999)
        listing['shipping'] = random.randint(5, 50)

        listings.append(listing)
    
    return listings


    
def generateTitle():
    adj = random.choice(wordlist.adjectives)
    noun = random.choice(wordlist.nouns)
    return f"{adj.capitalize()} {noun}"


def generateImage(img_count):
    img_url = 'https://picsum.photos/200'
    img_path = 'D://documents/School/CS50/cs50w/commerce/auctions/static/auctions/images/mock'
    filename = f"{img_count}.jpg"
    urllib.request.urlretrieve(img_url, f"{img_path}/{img_count}.jpg")
    return filename

def generateDescription():
    return gen.paragraph()
