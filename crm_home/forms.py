from django import forms
from .models import *


class ServiceForm(forms.ModelForm):
    name = forms.CharField(label='Услуга', label_suffix='', widget=forms.TextInput(attrs=({'class': 'form-control', 'required': 'required'})))
    show = forms.BooleanField(label_suffix='', label="Показывать в счетчиках")
    # unit = forms.CharField(label_suffix='', label="Ед. изм.", empty_value="Выберите")
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['id', ]
        labels = {
            'name': 'Услуга',
            'show': 'Показывать в счетчиках',
            'unit': 'Ед. изм.'
        }
        widgets = {
            'name': forms.TextInput(attrs=({'class': 'form-control', 'required': 'required'})),
            "unit": forms.Select(attrs={'class': 'form-select'})
        }






class UnitForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs=({'class': 'form-control'})),
                            empty_value='Введите единицы измерения', label_suffix='', label='Ед. изм.'
                            )
    class Meta:
        model = Unit
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs=({'class': 'form-control'}))
        }