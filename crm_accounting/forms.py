from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from houses.models import House, Flat
from users.models import CustomUser
from . import models
from .models import PersonalAccount


class PersonalAccountForm(forms.ModelForm):
    house = forms.ModelChoiceField(queryset=House.objects.all(),
                                   empty_label='Выберите...',
                                   widget=forms.Select(
                                       attrs={'class': 'form-select'}),
                                   label='Дом', required=False)
    status = forms.ChoiceField(
        choices=[('active', "Активен"), ('nonactive', "Неактивен")],
        widget=forms.Select(attrs={'class': 'form-select'}), label='Статус', )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PersonalAccountForm, self).__init__(*args, **kwargs)

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        account = models.PersonalAccount.objects.filter(account_number=account_number)
        if account.exists():
            if account.first() == self.instance:
                return account_number
            else:
                raise ValidationError(
                    'Этот лицевой счет уже существует'
                )
        return account_number

    def clean_flat(self):
        flat_id = self.cleaned_data.get('flat')
        if flat_id:
            if flat_id.personal_account == self.instance:
                return flat_id
            else:
                raise ValidationError(
                    'У этой квартиры уже есть лицевой счет.'
                )
        return flat_id

    class Meta:
        model = models.PersonalAccount
        exclude = ['balance', 'id']

        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'section': 'Секция',
            'flat': "Квартира"
        }


class TransactionForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=None),
                                   empty_label="Выберите...",
                                   widget=forms.Select(
                                       attrs={'class': 'form-select'}),
                                   label='Владелец квартиры',
                                   required=False)
    # manager = forms.ModelChoiceField(
    #     queryset=CustomUser.objects.filter(~Q(role=None)),
    #     empty_label="Выберите...",
    #     widget=forms.Select(
    #         attrs={'class': 'form-select'}),
    #     label='Менеджер')
    personal_account = forms.ModelChoiceField(queryset=
                                              PersonalAccount.objects.all(),
                                              empty_label="Выберите...",
                                              widget=forms.Select(
                                                  attrs=
                                                  {'class': 'form-select'}),
                                              label='Лицевой счет',
                                              required=False)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['manager'].empty_label = 'Выберите...'


    class Meta:
        model = models.Transaction
        exclude = ['id', ]
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                               'step': 0.1}),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'style': 'resize: none;',
                                             'rows': 5}),
            'completed': forms.CheckboxInput()
        }
        labels = {
            'payment_state': 'Статья',
            'amount': 'Сумма',
            'manager': 'Менеджер',
            'completed': 'Проведен',
            'comment': 'Комментарий'
        }
        error_messages = {
            'payment_state': {
                'required': 'Поле "Статья" обязательно к заполнению'
            },
            'amount': {
                'required': 'Поле "Сумма" обязательно к заполнению'
            },
            'number': {
                'unique': 'Пока вы дуумали, этот номер уже заняли!'
            }
        }