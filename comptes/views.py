from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm
from django.urls import reverse
from .models import Profile
# Create your views here.

#--------------Vue pour logger l'utilisateur-------------#
#regarder  le setting.py on a utilisé LOGIN_REDIRECT ET LOGOUT_REDIRECT
def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            informations = form.cleaned_data
            user = authenticate(request, username = informations['username']
                                , password=informations['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Bienvenue Mr')
                else:
                    return HttpResponse('Votre compte est desactivé')
        else:
            return HttpResponse('Formulaire invalide')
    else:
        form = LoginForm()
    return render(request, 'comptes/login.html', {'form': form})

#----------------Vue page destination apres le login---------------------#
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})


from .forms import LoginForm, UserRegistrationForm,UserEditForm,ProfileEditForm
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
        user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(
            request,
            'comptes/register_done.html',
            {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
    request,
    'comptes/register.html',
    {'user_form': user_form}
    )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
    instance=request.user,
    data=request.POST
    )
        profile_form = ProfileEditForm(
    instance=request.user.profile,
    data=request.POST,
    files=request.FILES
    )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'comptes/edit.html',{'user_form': user_form,'profile_form': profile_form})