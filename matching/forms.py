from django import forms
from .models import MatchingResult

# matching/forms.py

class MatchingForm(forms.Form):
    titre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Titre du sujet'})
    )
    fichier = forms.FileField()

