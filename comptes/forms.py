from django import forms


#-----------------Formulaire de loggin---------------------#

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#--------------------Formulaire pour enregistrer un user--------------#

from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
    label='Password',
    widget=forms.PasswordInput
    )
    password2 = forms.CharField(
    label='Repeat password',
    widget=forms.PasswordInput
    )
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email',]
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("mots de passe differents")
        return cd['password2']
    

from .models import Profile
class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']