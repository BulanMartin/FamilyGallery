from django import forms
from .models import Photo, PhotoGroup

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'group']

class PhotoGroupForm(forms.ModelForm):
    class Meta:
        model = PhotoGroup
        fields = ['name', 'description']