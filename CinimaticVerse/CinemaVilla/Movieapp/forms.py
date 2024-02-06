# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Movie,UserProfile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'date_of_birth', 'first_name', 'last_name', 'email']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }



#for movies
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description','movie_rating','quality','release_date', 'actors', 'category', 'trailer_link']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }