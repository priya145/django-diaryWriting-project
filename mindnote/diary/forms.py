from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Dailyfeed


class dailyfeedForm(forms.ModelForm):
    class Meta:
        model = Dailyfeed
        fields = ["title","blog"]

    
