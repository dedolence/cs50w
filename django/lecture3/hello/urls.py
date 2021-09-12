from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    #path('<str:name>', views.greet, name="greet"),
    path('<str:name>', views.greet2, name="greet2")
]