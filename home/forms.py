from django import forms
from django.utils.translation import gettext as _

class VideoUploadForm(forms.Form):
    location = forms.CharField(label='Video Location', max_length=64, required=False)
    file = forms.FileField()
