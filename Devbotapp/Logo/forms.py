# Devbotapp/forms.py

from .models import Logo
from django import forms



class LogoUploadForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ['image']
