from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:flight_id>', views.flight, name='pathName_flights'),
    path('<int:flight_id>/book', views.book, name="pathName_book")
]