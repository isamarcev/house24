from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from houses.models import House
from . import models
from .models import Role, CustomUser, Request


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password Input', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password repeat', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


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
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='',
                               label='Повторить пароль', required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='',
                               label='Пароль', required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='',
                                label='Фамилия')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'password', 'password2', 'role', 'email', 'phone', 'status']
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


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance:
            if len(password) == 0:
                raise ValidationError(
                    'Поле не может быть пустым!'
                )
        if len(password) > 0 and len(password) < 8:
            print('go')
            raise ValidationError(
                'Пароль не может быть меньше 8 символов.'
            )
        return password


    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            print('Ne sovpada')
            raise ValidationError(
                'Пароли не совпадают. Попробуйте снова'
            )
        return password2


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


class OwnerUserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='',
                                label='Повторить пароль', required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='',
                               label='Пароль', required=False)

    class Meta:
        model = CustomUser
        fields = ['photo', 'first_name', 'last_name', 'father_name', 'birthday', 'phone', 'viber', 'telegram', 'email', 'status',
                  'username', 'about', 'password', 'password2', ]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'viber': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': '13', 'style': 'resize: none;'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
        labels = {
            'photo': 'Сменить изображение',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'father_name': 'Отчество',
            'birthday': 'Дата рождения',
            'phone': "Телефон",
            'viber': "Viber",
            'telegram': "Telegram",
            'email': 'Email(логин)',
            'status': "Статус",
            'username': 'ID',
            'about': 'О владельце (заметки)'


        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance:
            if len(password) == 0:
                raise ValidationError(
                    'Поле не может быть пустым!'
                )
        if len(password) > 0 and len(password) < 8:
            print('go')
            raise ValidationError(
                'Пароль не может быть меньше 8 символов.'
            )
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                'Пароли не совпадают. Попробуйте снова'
            )
        return password2


class RequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RequestForm, self).__init__(*args, **kwargs)

    owner = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        queryset=CustomUser.objects.filter(role=None),
        empty_label="Выберите...", label='Владелец квартиры',
        required=True
    )

    class Meta:
        model = Request
        exclude = ['id', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs=({'class': 'form-control',
                                           "data-clocklet": ""}),
                                    format=('%H:%M')),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'style': 'resize: none;',
                                                 'rows': '8'}),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                                 'style': 'resize: none;',
                                                 'rows': '8'}),
            'type_master': forms.Select(attrs={'class': 'form-select'},
                                        choices=[("", "Выберите..."),
                                                 ("Сантехник", "Сантехник"),
                                                 ("Электрик", "Электрик"),
                                                 ("Слесарь", "Слесарь"),
                                                 ("Любой специалист",
                                                  "Любой специалист")]),
            'status': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'owner': 'Владелец квартиры',
            'master': 'Мастер',
            'description': "Описание",
            'flat': 'Квартира',
            'status': 'Статус',
            'comment': 'Комментарий',
            'type_master': 'Тип мастера'
        }

        error_messages = {
            'owner': {
                'required': "Это поле обязательно к заполнению"
            },
            'flat': {
                'required': "Это поле обязательно к заполнению"
            },
            'master': {
                'required': "Это поле обязательно к заполнению"
            },
        }


class RequestUserForm(forms.ModelForm):
    type_master = forms.ChoiceField(choices=[("", "Выберите..."),
                                                 ("Сантехник", "Сантехник"),
                                                 ("Электрик", "Электрик"),
                                                 ("Слесарь", "Слесарь"),
                                                 ("Любой специалист",
                                                  "Любой специалист")],
                                    widget=forms.Select(
                                        attrs={'class': 'form-select'}),
                                    required=False, label='Тип мастера')
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RequestUserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Request
        exclude = ['id', 'master', 'comment', 'status', 'owner']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs=({'class': 'form-control',
                                           "data-clocklet": ""}),
                                    format=('%H:%M')),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'style': 'resize: none;',
                                                 'rows': '4',
                                                 'placeholder':
                                                     'Опишите проблему'}),
        }
        labels = {
            'description': "Описание",
            'flat': 'Квартира',
            'date': "Дата работ",
            'time': "Время работ",
        }

        error_messages = {
            'flat': {
                'required': "Это поле обязательно к заполнению"
            },
        }


class MessageForm(forms.ModelForm):
    message_for_deptors = forms.BooleanField(required=False)
    message_address_house_id = forms.ModelChoiceField(
        queryset=House.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Всем...", required=False)

    class Meta:
        model = models.Message
        exclude = ['id', ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Тема сообщения:',
                                            }),
            'text': forms.Textarea(attrs={'placeholder': 'текст сообщения:'}),
            'message_address_house_id': forms.Select(
                attrs={'class': 'form-select'}),
        }
        error_messages = {
            'title': {
                'required': 'Это поле обязательно к заполнению!'
            }
        }



