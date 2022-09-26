from django import forms
from .models import *


class HouseForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Название')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label_suffix='', label='Адрес')
    image_1 = forms.ImageField(label_suffix='', label='Изображение #1. Развер: (522х350)', required=False)
    image_2 = forms.ImageField(label_suffix='', label='Изображение #2. Развер: (248х160)', required=False)
    image_3 = forms.ImageField(label_suffix='', label='Изображение #3. Развер: (248х160)', required=False)
    image_4 = forms.ImageField(label_suffix='', label='Изображение #4. Развер: (248х160)', required=False)
    image_5 = forms.ImageField(label_suffix='', label='Изображение #5. Развер: (248х160)', required=False)
    # users = forms.ModelChoiceField(required=False, queryset=CustomUser.objects.filter(role=True))

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


