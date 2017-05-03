# from django.forms import ModelForm, Form
from django import forms
from JJE_Waivers.models import WaiverClaim

class CancelForm(forms.Form):
    name = forms.CharField()