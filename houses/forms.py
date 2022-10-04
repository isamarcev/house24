from django import forms
from django.core.exceptions import ValidationError

from .models import *


class HouseForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Название')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Адрес')
    image_1 = forms.ImageField(label_suffix='', label='Изображение #1. Развер: (522х350)', required=False)
    image_2 = forms.ImageField(label_suffix='', label='Изображение #2. Развер: (248х160)', required=False)
    image_3 = forms.ImageField(label_suffix='', label='Изображение #3. Развер: (248х160)', required=False)
    image_4 = forms.ImageField(label_suffix='', label='Изображение #4. Развер: (248х160)', required=False)
    image_5 = forms.ImageField(label_suffix='', label='Изображение #5. Развер: (248х160)', required=False)

    class Meta:
        model = House
        fields = ['title', 'address', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5']
        exclude = ['id', ]


class SectionForm(forms.ModelForm):
    title = forms.CharField(label_suffix='', label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=False)

    class Meta:
        model = Section
        exclude = ['id', ]


class FloorForm(forms.ModelForm):
    title = forms.CharField(label_suffix='', label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=False)

    class Meta:
        model = Floor
        exclude = ['id', ]


class UserForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=True), label_suffix='', label='ФИО',
                                  widget=forms.Select(attrs={'class': 'form-select'}), empty_label="Выберите...")

    class Meta:
        model = CustomUser
        fields = ['name', ]


class FlatForm(forms.ModelForm):
    house = forms.ModelChoiceField(queryset=House.objects.all(), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Дом')
    owner = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=None), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Владелец')
    tariff = forms.ModelChoiceField(queryset=Tariff.objects.all(), empty_label='Выберите...',
                                   widget=forms.Select(attrs={'class': 'form-select'}), label='Тариф')

    class Meta:

        model = Flat
        fields = ['number', 'area', 'house', 'section', 'floor', 'owner', 'tariff']
        labels = {
            'number': "Номер квартиры",
            'area': "Площадь (кв.м.)",
            'section': "Секция",
            'floor': "Этаж",
        }
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PersonalAccountForm(forms.ModelForm):
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     label='Лицевой счет', required=False)

    class Meta:
        model = PersonalAccount
        fields = ['account_number']

    def clean_account_number(self):
        account = self.cleaned_data.get('account_number')
        if not account.isdigit():
            if account == '':
                pass
            else:
                raise ValidationError(
                    "Лицевой счет должен состоять из цифр."
                )
        return account


