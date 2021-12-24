from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt    # to make the watchlist AJAX request work, which doesn't use a CSRF token
from .models import User, Listing, Bid, Comment, Category, Watchlist
from math import floor

# form handling
from .forms import NewListingForm

#for testing
from . import wordlist
import random
import requests
from essential_generators import DocumentGenerator

from django.utils import timezone
from datetime import timedelta


gen = DocumentGenerator()

# globals
LOCAL_TIMEZONE = timezone.now().astimezone().tzinfo
LISTING_EXPIRATION_DAYS = 14        # global value for how long listings are active
MESSAGE_LISTING_DELETED = "Listing {} has been deleted."
MESSAGE_LISTING_EDIT_PROHIBITED = "Listing {} cannot be edited because it currently has bids placed on it. However, you can still delete this listing."



def index(request, message_code=None, id=None):
    message = ''
    if request.user.is_authenticated:

        # parse message, if any
        if message_code:
            if message_code == MESSAGE_LISTING_DELETED:
                message = MESSAGE_LISTING_DELETED.format(id)
            elif message_code == MESSAGE_LISTING_EDIT_PROHIBITED:
                message = MESSAGE_LISTING_EDIT_PROHIBITED.format(id)

        active_listings = Listing.objects.filter(user_id=request.user.id)
        return render(request, "auctions/index.html", {
            'listings': active_listings,
            'watchlist': getWatchlist(request.user.id),
            'alert_warning': message
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


@login_required
def create_listing(request):
    # if GET, display new listing form
    if request.method == "GET":
        form = NewListingForm()
        # categories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            # 'categories': categories
            'form': form
        })

    # TODO: move this to the views.preview_listing() method     
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
            # create a form instance with POST data
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
                return HttpResponseRedirect(reverse('view_listing', args=[instance.id]))
            else:
                return render(request, 'auctions/previewListing.html', {
                    'listing': instance,
                    'form': form,
                    'form_controls': False
                })


@login_required
def place_bid(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("index"))
    else:
        listing_id = request.POST["listing-id"]
        listing_bundle = getListing(request, listing_id)
        bid = request.POST["bid"]
        if bid.isdigit() == False:
            return render(request, "auctions/viewListing.html", {
                'listing_bundle': listing_bundle,
                'bid_message': 'Bid must be whole numbers.'
            })
        else:
            if int(bid) <= listing_bundle["listing"].current_bid:
                return render(request, "auctions/viewListing.html", {
                    'listing_bundle': listing_bundle,
                    'bid_message': 'Bid must larger than the current bid.'
                })
            else:
                new_bid = Bid.objects.create(amount=int(bid), user=request.user, listing=listing_bundle["listing"])
                new_bid.save()
                return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))

@login_required
def edit_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "GET":
        # check to make sure there aren't any bids on this listing to prevent bait-and-switch
        if listing.current_bid != listing.starting_bid:
            return HttpResponseRedirect(reverse("index_with_message", args=[MESSAGE_LISTING_EDIT_PROHIBITED, listing.title]))
        else:
            form = NewListingForm(instance=listing)
            return render(request, "auctions/editListing.html", {
                'form': form,
                'listing': listing
            })
    else:
        form = NewListingForm(request.POST, instance=listing)
        if not form.is_valid():
            return render(request, "auctions/editListing.html", {
                'form': form,
                'listing': listing
            })
        else:
            form.save()
            return HttpResponseRedirect(reverse("view_listing", args=[listing.id]))


@login_required
def delete_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "GET":
        return render(request, 'auctions/deleteListing.html', {
            'listing': listing
        })
    else:
        title = listing.title
        listing.delete()
        return HttpResponseRedirect(reverse("index_with_message", 
            args=[MESSAGE_LISTING_DELETED, title]))


def listings(request):
    if request.method == "GET":
        listings_raw = Listing.objects.all()
        listings = [getListing(request, None, listing) for listing in listings_raw]
        return render(request, "auctions/listings.html", {
            'listing_bundles': listings,
            'watchlist': getWatchlist(request.user.id)
        })


def listing_page(request, listing_id):
    listingBundle = getListing(request, listing_id)
    return render(request, "auctions/viewListing.html", {
        'listing_bundle': listingBundle
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
    if not request.user.is_authenticated:
        response = dict(message="You must be logged in to do that.", button_text="Add to Watchlist")
    else:
        listing = Listing.objects.get(id=listing_id)
        watched_item, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
        if created:
            response = dict(message='Added to watchlist.', button_text='Watching')
        else:
            watched_item.delete()
            response = dict(message="Removed from watchlist.", button_text='Add to Watchlist')
    return JsonResponse(response)


def view_all_users(request):
    return HttpResponseRedirect(reverse(''))


def view_user(request, username):
    user = User.objects.get(username=username)
    listings = Listing.objects.filter(user_id=user.id)
    return render(request, "auctions/user.html", {
        "user": user,
        "listings": listings
    })

# //////////////////////////////////////////////////////
# UTILITY FUNCTIONS
# //////////////////////////////////////////////////////

def getHighestBid(listing) -> Bid:
    bids = Bid.objects.filter(listing=listing).order_by('-amount')
    return bids.first()

def getListing(request, id=None, listing=None) -> dict:
    if not listing:
        listing = Listing.objects.get(pk=id)
    owner_controls = True if listing.user == request.user else False
    watch_options = True if owner_controls == False else True
    watchlist = getWatchlist(request.user.id)
    watching_currently = True if listing in watchlist else False
    expiration_bundle = checkExpiration(listing)
    current_bid = getHighestBid(listing)
    return {
        'listing': listing,
        'owner_controls': owner_controls,
        'watch_options': watch_options,
        'watching_currently': watching_currently,
        'expiration_bundle': expiration_bundle,
        'current_bid': current_bid
    }


def checkExpiration(listing) -> dict:
    """Make sure the listing is still active according to its creation timestamp.
    Irrelevant, but for my own notes:
    Due to the db being sqlite, the timestamp is a naive date; i.e. it does not carry with it any timezone information.
    By default Django creates objects using UTC time format.
    LOCAL_TIMEZONE stores the timezone as a string in ISO format, to be used for converting UTC timestamps to local user timezones.
    """
    expiration_date = listing.timestamp + timedelta(days=LISTING_EXPIRATION_DAYS)
    today = timezone.now()
    difference = (expiration_date - today)      # e.g. 13 days, 22:18:29.642879.
    s = difference.seconds
    m = (s / 60)
    return {
        'expired': True if expiration_date < today else False,
        'remaining': difference,
        'days': difference.days,
        'hours': floor(m / 60),
        'minutes': floor((s / 60) % 60),
        'seconds': floor(s % 60)
    }
    

def getWatchlist(user_id):
    """Gets a user's watchlist based on their ID.
    For a plain descriptive string of the listing being watched, one could simply
    get a queryset from the join table itself, which Django nicely cross-references
    to fill in the details. But this doesn't return an object with accessible
    properties like listing.title, or listing.description; hence, separate DB queries.
    """""" 
    watch_joinset = Watchlist.objects.filter(user_id=user_id)
    watchlist = []
    for watch_item in watch_joinset:
        watchlist.append(Listing.objects.get(pk=watch_item.listing_id))
    return watchlist """
    watchlist_raw = Watchlist.objects.filter(user=user_id)



# //////////////////////////////////////////////////////
# TESTING FUNCTIONS
# //////////////////////////////////////////////////////

def test_bidding(request):
    listing_id = 32     # arbitrary active listing
    listing_bundle = getListing(request, listing_id)
    bids = Bid.objects.filter(listing=listing_bundle['listing']).order_by('-amount')
    highest_bid = bids.first()  # returns None if no bids are found
    return render(request, "auctions/tests/testBidding.html", {
        'listing-bundle': listing_bundle,
        'bids': bids,
        'highest_bid': highest_bid
    })


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

    
def datetime(request):
    if request.user.is_superuser:    
        # arbitrary listing
        listing = Listing.objects.get(pk=48)
        timezone.activate(LOCAL_TIMEZONE)
        creation_date = listing.timestamp # format: 2021-12-03 19:28:45.637086
        expiration_date = listing.timestamp + timedelta(days=LISTING_EXPIRATION_DAYS)
        date_difference = (expiration_date - creation_date).days
        today = timezone.now()
        until_expiration = (expiration_date - today).days
        tz = timezone.get_current_timezone()
        tz_info = timezone.now().astimezone().tzinfo
        lt = timezone.localtime()
        tz_now = timezone.now()
        expiredCheck = checkExpiration(listing)
        return render(request, "auctions/datetime.html", {
            'creation_date': creation_date,
            'creation_tz': creation_date.astimezone().tzinfo,
            'today_tz': today.astimezone().tzinfo,
            'expiration_date': expiration_date,
            'expiration_tz': expiration_date.astimezone().tzinfo,
            'date_difference': date_difference,
            'now': today,
            'until_expiration': until_expiration,
            'tz': tz,
            'tz_info': tz_info,
            'lt': lt,
            'lt_tz': lt.tzinfo,
            'tz_now': tz_now,
            'tz_now_tzinfo': tz_now.tzinfo,
            'expired': expiredCheck['expired'],
            'remaining': expiredCheck['remaining'],
            'days_remaining': expiredCheck['remaining'].days,
            'hours_remaining': expiredCheck['hours'],
            'minutes_remaining': expiredCheck['minutes'],
            'seconds_remaining': expiredCheck['seconds']
        })
    else:
        return HttpResponseRedirect(reverse("index"))