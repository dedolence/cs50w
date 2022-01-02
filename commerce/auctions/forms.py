# Not going to use this after all, as I'd prefer writing the form manually to have better control over styles with Bootstrap

from django import forms
from django.forms import ModelForm
from .models import Category
from .models import Listing

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'starting_bid', 'shipping', 'category']
