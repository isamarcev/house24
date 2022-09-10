from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from . import models


class RegisterUserForm(UserCreationForm):
    # email = forms.EmailField(label='Електронная почта', widget=forms.EmailInput(attrs={'class':'form-input'}))
    # username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-input'}))
    # first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-input'}))
    # sex = forms.ChoiceField(choices=([('m', 'male'), ('f', 'female')]))
    password1 = forms.CharField(label='Password Input', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password repeat', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    # class Meta:
    #     model = models.CustomUser
    #     fields = ['email', 'username', 'last_name', 'first_name', 'sex']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                            'placeholder': 'Email или ID'}))
    password = forms.CharField(label='Password Input', widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                         'placeholder': 'Пароль'}))
