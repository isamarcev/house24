from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from . import models
from .models import Role


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

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role

        exclude = ['id', 'name']
        labels = {
            'name': "Роль",
            'statistics': "Статистика",
            'cashbox': "Касса",
            'invoice': "Квитанции",
            'personal_account': "Лицевые счета",
            'flat': "Квартиры",
            'owner': "Владельцы квартир",
            'house': "Дома",
            'message': "Сообщения",
            'application': "Заявки вызова мастера",
            'meter': "Счетчики",
            'site_management': "Управление сайтом",
            'service': "Услуги",
            'tariff': "Тарифы",
            'role': "Роли",
            'users': "Пользователи",
            'requisites': "Платежные реквизиты",
        }
        widgets = {
            # 'name': forms.NullBooleanField,
            'statistics': forms.CheckboxInput,
            'cashbox': forms.CheckboxInput,
            'invoice': forms.CheckboxInput,
            'personal_account': forms.CheckboxInput,
            'flat': forms.CheckboxInput,
            'owner': forms.CheckboxInput,
            'house': forms.CheckboxInput,
            'message': forms.CheckboxInput,
            'application': forms.CheckboxInput,
            'meter': forms.CheckboxInput,
            'site_management': forms.CheckboxInput,
            'service': forms.CheckboxInput,
            'tariff': forms.CheckboxInput,
            'role': forms.CheckboxInput,
            'users': forms.CheckboxInput,
            'requisites': forms.CheckboxInput,
        }
