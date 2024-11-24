from django import forms
# from django.forms import ModelForm
from .models import Listing

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['description', 'address', 'category', 'land_size', 'building_size', 'bedrooms', 'bathrooms', 'latitude', 'longitude', 'price']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',  # Apply Bootstrap class
                'rows': 3,  # Set number of rows to limit height
                'placeholder': 'Enter a brief description of the listing',  # Optional placeholder text
            }),
        }
