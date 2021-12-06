from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import get_template
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt    # to make the watchlist AJAX request work, which doesn't use a CSRF token

from .models import User, Listing, Bid, Comment, Category, Watchlist


# form handling
from .forms import NewListingForm
from django.core.files.uploadedfile import SimpleUploadedFile

#for testing
from . import wordlist
import random
import urllib.request
import requests
from essential_generators import DocumentGenerator
gen = DocumentGenerator()

def index(request):
    if request.user.is_authenticated:    
        active_listings = Listing.objects.filter(user_id=request.user.id)
        return render(request, "auctions/index.html", {
            'listings': active_listings,
            'watchlist': getWatchlist(request.user.id)
        })
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # page to redirect to
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('index')

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if 'next' in request.GET:
            next = request.GET['next']
        else:
            next = None
            
        return render(request, "auctions/login.html", {
            'next': next
        })


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


def create_listing(request):
    # if GET, display new listing form
    if request.method == "GET":
        form = NewListingForm()
        # categories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            # 'categories': categories
            'form': form
        })

    # else if POST, preview listing for changes or add to DB
    elif request.method == "POST":

        # check if we need to generate a random listing:
        if 'random' in request.POST:
            form = NewListingForm(generateListing(1))
        else:
            # create form instance
            form = NewListingForm(request.POST)
        
        # validate form
        if not form.is_valid():
            # errors were found so return the form to the initial listing form page
            return render(request, "auctions/createListing.html", {
                'form': form
            })
        
        else:
            # create a form insance with POST data
            instance = form.save(commit=False)
            # attach user to the form instance
            instance.user = request.user
            instance.current_bid = instance.starting_bid
            # check to see if we need to preview or submit
            if 'submit' in request.POST:
                # add to DB
                instance.save()
                # include many-to-many relationships
                form.save_m2m()
                return HttpResponseRedirect(reverse('listing', args=[instance.id]))
            else:
                return render(request, 'auctions/previewListing.html', {
                    'listing': instance,
                    'form': form,
                    'form_controls': False
                })


def listings(request):
    return render(request, "auctions/listings.html", {
        'listings': Listing.objects.all(),
        'watchlist': getWatchlist(request.user.id)
    })

def listing_page(request, listing_id):
    return render(request, "auctions/listing.html", {
        'listing': Listing.objects.get(pk=listing_id)
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })

def category(request, category_id):
    category_title = Category.objects.get(id=category_id)
    category_listings = Listing.objects.filter(category_id=category_id)
    return render(request, "auctions/category.html", {
        'category_title': category_title,
        "category_listings": category_listings
    })

@csrf_exempt
def watch_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watched_item = Watchlist(user=request.user, listing=Listing.objects.get(id=listing_id))
    watched_check = Watchlist.objects.get(listing=listing, user=request.user)

    # check to see if the watched_item exists within the user's watchlist already
    if watched_check is None:
        watched_item.save()
        return HttpResponse("Added to watchlist!")
    else:
        watched_check.delete()
        return HttpResponse("Removed from watchlist.")

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
    user = User.objects.get(username=username)
    listings = Listing.objects.filter(user_id=user.id)
    return render(request, "auctions/user.html", {
        "user": user,
        "listings": listings
    })

def view_all_users(request):
    return HttpResponseRedirect(reverse(''))





# testing methods below
def viewMockup(request):
    titles = generateListing(10)
    return render(request, "auctions/mockup.html", {
        "titles": titles
    })


def generateListing(amount):
    listings = []
    for i in range(amount):
        listing = {
            'title': generateTitle(),
            'image_url': generateImage(),
            'description': generateDescription()[0:500],
            'starting_bid': random.randint(1,9999),
            'shipping': random.randint(5, 50),
            'category': random.randint(1, 8)
        }
        listings.append(listing)
    
    return listings if (amount>1) else listings[0]


    
def generateTitle():
    adj = random.choice(wordlist.adjectives)
    noun = random.choice(wordlist.nouns)
    return f"{adj.capitalize()} {noun}"

def generateImage():
    # sorta inefficient because the api loads a random image but only looks at the response headers for the id to generate a static URL,
    # so the image is ultimately served twice, first here and again when its absolute URL is called :(
    # but since this is only for testing purposes really it doesn't matter so much, and it's only 200px square images
    image_api = requests.get('https://picsum.photos/200')
    image_id = image_api.headers['picsum-id']
    return f'https://picsum.photos/id/{image_id}/200'
    
def generateDescription():
    return gen.paragraph()

def picsum(request):
    image_api = requests.get('https://picsum.photos/200')
    image_id = image_api.headers['picsum-id']
    image_url = f'https://picsum.photos/id/{image_id}/200'
    return render(request, 'auctions/tests/picsum.html', {
        'url': image_url
    })

def ajax_test(request):
    return render(request, "auctions/tests/ajax.html")

def ajax_return(request):
    return HttpResponse("Here's a message")