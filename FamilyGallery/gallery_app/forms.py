from django import forms
from .models import Photo, Group
from django.forms.widgets import FileInput

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'group']

class PhotoGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class UploadFolderForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    images = MultipleFileField()
