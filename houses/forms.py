from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db.models import Q

from .models import *


class HouseForm(forms.ModelForm):
    image_error_messages = {
        "invalid_image":
             'Файл вложенного формата недопустим. '
             'Выберите файл с форматорми .png , .jpg .jpeg.'
    }
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Название')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Адрес')
    image_1 = forms.ImageField(label_suffix='',
                               label='Изображение #1. Размер: (522х350)',
                               required=False,
                               error_messages=image_error_messages)
    image_2 = forms.ImageField(label_suffix='',
                               label='Изображение #2. Размер: (248х160)',
                               required=False,
                               error_messages=image_error_messages)
    image_3 = forms.ImageField(label_suffix='',
                               label='Изображение #3. Размер: (248х160)',
                               required=False,
                               error_messages=image_error_messages)
    image_4 = forms.ImageField(label_suffix='',
                               label='Изображение #4. Размер: (248х160)',
                               required=False,
                               error_messages=image_error_messages)
    image_5 = forms.ImageField(label_suffix='',
                               label='Изображение #5. Размер: (248х160)',
                               required=False,
                               error_messages=image_error_messages)
    good_format = ['png', 'jpg', 'jpeg']
    class Meta:
        model = House
        fields = ['title', 'address', 'image_1', 'image_2', 'image_3',
                  'image_4', 'image_5']
        exclude = ['id', ]
        error_messages = {
            'image_1': {"invalid_image":
                        'Файл вложенного формата недопустим. '
                        'Выберите файл с форматорми .png , .jpg .jpeg.'}
            }

    def clean_image_1(self):
        image = self.cleaned_data.get('image_1')
        if image:
            w, h = get_image_dimensions(image)
            if w != 522 and h != 350:
                raise ValidationError(
                    'Загрузите изображение правильного размера'
                )
            format_file = image.name.split('.')[-1]
            if format_file not in self.good_format:
                raise ValidationError(
                    'Файл вложенного формата недопустим. '
                    'Выберите файл с форматорми .png , .jpg .jpeg'
                )
        return image

    def clean_image_2(self):
        image = self.cleaned_data.get('image_2')
        if image:
            w, h = get_image_dimensions(image)
            if w != 248 and h != 160:
                raise ValidationError(
                    'Загрузите изображение правильного размера'
                )
            format_file = image.name.split('.')[-1]
            if format_file not in self.good_format:
                raise ValidationError(
                    'Файл вложенного формата недопустим. '
                    'Выберите файл с форматорми .png , .jpg .jpeg'
                )
        return image

    def clean_image_3(self):
        image = self.cleaned_data.get('image_3')
        if image:
            w, h = get_image_dimensions(image)
            if w != 248 and h != 160:
                raise ValidationError(
                    'Загрузите изображение правильного размера'
                )
            format_file = image.name.split('.')[-1]
            if format_file not in self.good_format:
                raise ValidationError(
                    'Файл вложенного формата недопустим. '
                    'Выберите файл с форматорми .png , .jpg .jpeg'
                )
        return image

    def clean_image_4(self):
        image = self.cleaned_data.get('image_4')
        if image:
            w, h = get_image_dimensions(image)
            if w != 248 and h != 160:
                raise ValidationError(
                    'Загрузите изображение правильного размера'
                )
            format_file = image.name.split('.')[-1]
            if format_file not in self.good_format:
                raise ValidationError(
                    'Файл вложенного формата недопустим. '
                    'Выберите файл с форматорми .png , .jpg .jpeg'
                )
        return image

    def clean_image_5(self):
        image = self.cleaned_data.get('image_5')
        if image:
            w, h = get_image_dimensions(image)
            if w != 248 and h != 160:
                raise ValidationError(
                    'Загрузите изображение правильного размера'
                )
            format_file = image.name.split('.')[-1]
            if format_file not in self.good_format:
                raise ValidationError(
                    'Файл вложенного формата недопустим. '
                    'Выберите файл с форматорми .png , .jpg .jpeg'
                )
        return image


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
    name = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(~Q(role=None)),
        label_suffix='', label='ФИО',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Выберите...")

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


