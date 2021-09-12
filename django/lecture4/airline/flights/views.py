from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Flight, Passenger
from django.urls import reverse


def index(request):
    return render(request, 'flights/index.html', {
        'flights': Flight.objects.all()
    })

def flight(request, flight_id):
    #pk = primary key
    flight = Flight.objects.get(pk=flight_id)
    return render(request, 'flights/flight.html', {
        'flight': flight,
        'passengers': flight.passengers.all(),
        'non_passengers': Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    # if posting, i.e. adding new data to db
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST['passenger']))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('pathName_flights', args=(flight.id,)))
