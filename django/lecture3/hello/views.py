from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'hello/index.html')  # render dynamic template

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}.")

def greet2(request, name):
    return render(request, 'hello/greet2.html', {
        'name': name.capitalize()
    })