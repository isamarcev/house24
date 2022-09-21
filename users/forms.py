from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from . import models
from .models import Role, CustomUser


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

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BaseModelForm, self).__init__(*args, **kwargs)


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='',
                               label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='',
                               label='Повторить пароль')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='',
                                label='Фамилия')
    # role = forms.ModelChoiceField(queryset=Role.objects.all().values_list('id', 'name'),
    #                               )
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['id', 'date_joined',]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})

        }
        labels = {
            'status': "Статус",
            'role': "Роль",
            'phone': "Телефон",
            'email': 'Email(логин)'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                'Пароли не совпадают. Попробуйте снова'
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


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


class SearchUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', ]
