from django import forms
from .models import Location

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['image', 'place', 'description', 'longitude', 'latitude']
