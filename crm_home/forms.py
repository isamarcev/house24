from django import forms
from django.core.exceptions import ValidationError

from houses.models import House
from .models import *


class ServiceForm(forms.ModelForm):
    name = forms.CharField(label='Услуга', label_suffix='',
                           error_messages=
                           {'required': 'Поле не может быть пустым.'},
                           widget=forms.TextInput(
                            attrs=({'class': 'form-control'})))
    show = forms.BooleanField(label_suffix='', label="Показывать в счетчиках",
                              required=False)
    # unit = forms.CharField(label_suffix='', label="Ед. изм.", empty_value="Выберите")
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['id', ]
        labels = {
            'unit': 'Ед. изм.'
        }
        widgets = {
            'name': forms.TextInput(attrs=({'class': 'form-control', 'required': 'required'})),
            "unit": forms.Select(attrs={'class': 'form-select '})
        }

    # def clean_name(self):
    #     new_name = self.cleaned_data['name']
    #     if not new_name:
    #         raise ValidationError('Это обязательное поле!.')
    #     return new_name


class UnitForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs=({'class': 'form-control'})),
                             label_suffix='', label='Ед. изм.'
                            )
    class Meta:
        model = Unit
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs=({'class': 'form-control'}))
        }


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'describe']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'describe': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'style': 'resize: none'})
        }
        labels = {
            'name': 'Название тарифа',
            'describe': "Описание тарифа"
        }


class TariffServiceForm(forms.ModelForm):
    class Meta:
        model = TariffService
        fields = ['price', 'service',]
        exclude = ['id',]
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select select-choose'}),
            'price': forms.TextInput(attrs={'class': 'form-control'})

        }
        error_messages = {
            'price': {'null': 'Введите цену за услугу.',
                      'blank': 'Введите цену за услугу.',
                        'invalid': 'Поле должно быть числом.'
                      }
        }

    def clean_price(self):
        new_price = self.cleaned_data['price']
        service = self.cleaned_data['service']
        if service:
            if new_price is None:
                raise ValidationError('Поле не может быть пустым!')
        return new_price


class RequisitesForm(forms.ModelForm):
    class Meta:
        model = Requisites
        fields = ['title', 'info']
        labels = {
            'title': "Название компании",
            'info': "Информация"
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'style': 'resize: none;'})
        }


class PaymentStateForm(forms.ModelForm):
    title = forms.CharField(label_suffix='', label="Название",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))

    type = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-select'}), label_suffix='',
        label="Приход/расход",
        choices=[("Приход", "Приход"), ("Расход", "Расход")])

    class Meta:
        model = PaymentState
        fields = ['title', 'type']


class CounterDataForm(forms.ModelForm):
    date = forms.DateField()
    house = forms.ModelChoiceField(empty_label='Выберите',
                                   queryset=House.objects.all(),
                                   label='Дом',
                                   widget=forms.Select(
                                       attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CounterDataForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CounterData
        exclude = ['id', ]
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            # 'date': 'form-control',
            # 'status': 'form-control',
            # 'data': 'form-se',
        }



