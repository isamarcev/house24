from django import forms
from django.core.exceptions import ValidationError

from houses.models import House, Flat
from .models import *


class PersonalAccountForm(forms.ModelForm):
    house = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Дом')
    status = forms.ChoiceField(choices=[('active', "Активен"), ('nonactive', "Неактивен")],
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Статус', )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PersonalAccountForm, self).__init__(*args, **kwargs)

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        account = PersonalAccount.objects.filter(account_number=account_number)
        if account.exists():
            raise ValidationError(
                'Этот лицевой счет уже существует'
            )
        return account_number

    def clean_flat(self):
        flat_id = self.cleaned_data.get('flat')
        print(flat_id)
        if flat_id:
            if flat_id.personal_account:
                raise ValidationError(
                    'У этой квартиры уже есть лицевой счет.'
                    )
        else:
            raise ValidationError(
                'Поле квартиры обязательно к заполнению.'
            )
        return flat_id


    class Meta:
        model = PersonalAccount
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





