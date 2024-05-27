from django import forms
from .models import Photo, Group

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'group']

class PhotoGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']