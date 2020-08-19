from django import forms
from core.models import ShortenedURL


class ShortenURLForm(forms.ModelForm):
    expanded_url = forms.CharField(
        label='Full URL'
    )

    class Meta:
        model = ShortenedURL
        fields = ('expanded_url',)
