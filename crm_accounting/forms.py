from django import forms
from django.core.exceptions import ValidationError

from houses.models import House
from .models import *


class PersonalAccountForm(forms.ModelForm):
    house = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Дом')
    status = forms.ChoiceField(choices=[('active', "Активен"), ('nonactive', "Неактивен")],
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Статус', )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PersonalAccountForm, self).__init__(*args, **kwargs)


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




