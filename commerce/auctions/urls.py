from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),        # the user's page
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/", views.listings, name="all_listings"),     # django automatically appends a / if it's left out, which is convenient. so /listings works as well as /listings/
    path("listings/<int:listing_id>", views.listing_page, name="listing"),
    path("categories/", views.categories, name="categories"),
    path("categories/<category>", views.category, name="category"),
    path("create/", views.create_listing, name="create_listing"),
    path("users/<str:username>", views.view_user, name="view_user"),
    # for testing look
    path("mockup/", views.viewMockup, name="mockup")
]
