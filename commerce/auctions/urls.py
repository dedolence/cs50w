from django.conf.urls import include
from django.urls import path, include


from . import views

urlpatterns = [
    path("", views.index, name="index"),        # the user's page
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/", views.listings, name="all_listings"),     # django automatically appends a / if it's left out, which is convenient. so /listings works as well as /listings/
    path("listings/view/<int:listing_id>", views.listing_page, name="view_listing"),
    path("watch/<int:listing_id>", views.watch_listing, name="watch_listing"),     # AJAX view
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("create/", views.create_listing, name="create_listing"),
    path("edit/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("accounts/<str:username>", views.view_user, name="view_user"),
    # for testing look
    path("mockup/", views.viewMockup, name="mockup"),
    path("picsum/", views.picsum, name="picsum"),
    path("ajax/", views.ajax_test, name="ajax_test"),
    path("ajax/request/", views.ajax_return, name="ajax_return")
]
