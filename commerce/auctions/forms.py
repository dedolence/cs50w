from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, required=True)
    description = forms.CharField(label="Description", max_length=200, required=True)
    image = forms.ImageField(label="Photo", required=False)
    starting_bid = forms.IntegerField(label="Starting Bid", required=True)