from django import forms

from advertiser_management.models import Ad


class CreateAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['advertiser', 'title', 'image', 'landing_url']