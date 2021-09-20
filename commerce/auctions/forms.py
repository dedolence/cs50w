from django import forms
from django.forms import ModelForm
from .models import Category
from .models import Listing

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'starting_bid', 'category']

class OldNewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, required=True)
    description = forms.CharField(label="Description", max_length=200, required=True)
    image = forms.ImageField(label="Photo", required=False)
    starting_bid = forms.FloatField(required=True, label="Starting bid", min_value=.01, max_value=9999.99)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
