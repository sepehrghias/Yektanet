from django import forms

from advertiser_management.models import Ad , View



class CreateAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['advertiser', 'title', 'image', 'landing_url']