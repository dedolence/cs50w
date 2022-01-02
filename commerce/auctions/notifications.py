from . import strings
from .models import Notification
from django.urls import reverse


def generate_notification(user, type, icon, message):
    """Generate and return an alert box. The color (and therefore priority) is
    set by 'type' to correspond to Bootrstrap 5.0 'alert alert-{type}' class.
    'Icon' refers to the Bootrstrap icon library.
    """
    content = (strings.MESSAGE_INFORMATION).format(icon=icon, message=message)
    notification = Notification.objects.create(user=user, content=content, type=type)
    notification.save()
    return notification


def get_notifications(user):
    return Notification.objects.filter(user=user)


def purge_notification(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.delete()


def notify_winner(user, listing):
    listing_title = listing.title
    listing_url = reverse('view_listing', args=[listing.id])
    shopping_cart_url = reverse('shopping_cart')
    message = (strings.MESSAGE_NOTIFY_WINNER).format(
        listing_url=listing_url, listing_title=listing_title, 
        shopping_cart_url=shopping_cart_url)
    generate_notification(user, 'success', 'none', message)


