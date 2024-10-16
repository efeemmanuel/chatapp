from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import *


User=get_user_model()

class UserForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 450px;', 'placeholder': 'Enter username'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 450px;', 'placeholder': 'Enter firstname'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control','style': 'max-width: 450px;', 'placeholder': 'Enter lastname'}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'max-width: 450px;', 'placeholder': 'Set password'}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'max-width: 450px;', 'placeholder': 'Confirm password'}))
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]
        




class ProfileForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Lastname'}))
    class Meta:
        model = Profile
        fields = ["username", "first_name", "last_name", "profile_picture"]
        


