
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


from django import forms

class MatchingForm(forms.Form):
    titre = forms.CharField(label='Titre du sujet', max_length=200)
    sujet = forms.FileField(label='Charger le fichier du sujet')


class MatchingResult(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    texte_nettoye = models.TextField(default=" ")
    niveau_pred = models.CharField(max_length=50, default='Inconnu')
    success_rate = models.FloatField()
    date_analyse = models.DateTimeField(auto_now_add=True)
