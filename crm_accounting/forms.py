from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from django.forms import modelformset_factory

from crm_home.models import Unit, Service
from houses.models import House, Flat
from users.models import CustomUser
from . import models
from .models import PersonalAccount, get_next_invoice, get_next_account


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

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if number:
            if not number.isdigit():
                raise ValidationError(
                    'Номер должен состоять из цифр.'
                )
        return number


class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = 'Выберите...'
        self.fields['status'].empty_label = 'Выберите...'
        self.fields['tariff'].empty_label = 'Выберите...'

    class Meta:
        model = models.Invoice
        exclude = ['id']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-select'}),
            'personal_account':
                forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tariff': forms.Select(attrs={'class': 'form-select'}),
            'period_start': forms.DateInput(attrs={'class': 'form-control'}),
            'period_end': forms.DateInput(attrs={'class': 'form-control'}),
            'payment_state': forms.CheckboxInput(),
        }
        labels = {
            'house': 'Дом',
            'section': 'Секция',
            'personal_account': 'Лицевой счет',
            'status': 'Статус',
            'tariff': 'Тариф',
            'period_start': 'Период с',
            'period_end': 'Период по',
            'payment_state': 'Проведена',
            'flat': 'Квартира',
        }

        error_messages = {
            'number': {
                'unique': "Квитанцция с таким номером уже существует"
            },
            'house': {
                'blank': "Это поле обязательно к заполнению.",
                'required' :"Это поле обязательно к заполнению."
            },
            'section': {
                'blank': "Это поле обязательно к заполнению.",
                'required':"Это поле обязательно к заполнению."

        },
            'flat': {
                'blank': "Это поле обязательно к заполнению.",
                'required':"Это поле обязательно к заполнению."
            },
        }

    def clean_personal_account(self):
        personal_account = self.cleaned_data.get('personal_account')
        if not personal_account:
            personal_account = get_next_account()
        flat = self.cleaned_data.get('flat')
        if flat.personal_account:
            if flat.personal_account.account_number == personal_account:
                return personal_account
            else:
                return flat.personal_account.account_number
        else:
            new_account = PersonalAccount.objects.create(
                account_number=personal_account)
            new_account.save()
            flat.personal_account = new_account
            new_account.flat = flat
            return personal_account

    def calculate_invoice(self, form_class, **kwargs):
        """Calculate balance of PERSONAL ACCOUNT"""
        type_of_form = kwargs.get('type')
        instance_status = kwargs.get('status')
        instance_payment_state = kwargs.get('payment_state')
        form_status = form_class.instance.status
        form_payment_state = form_class.instance.payment_state
        account = form_class.instance.flat.personal_account
        qwer = models.Transaction.objects.filter(personal_account=account,
                                                 payment_state__type='in',
                                                 completed=True).\
            aggregate(Sum('amount')).get('amount__sum')
        print(qwer)
        rewq = models.Invoice.objects.filter(personal_account=account,
                                             payment_state=True,
                                             status='Оплачена').\
            aggregate(Sum('amount')).get('amount__sum')
        if not rewq:
            rewq = 0
        if not qwer:
            qwer = 0
        operation = qwer - rewq
        print(operation)
        account.balance = operation
        # # account.balance =
        # # income_for_account = PersonalAccount.objects.filter(id=form_status.instance.flat.personal_account.id)
        # if type_of_form == 'update':
        #     if instance_status == form_status and \
        #         instance_payment_state == form_payment_state:
        #         pass
        #     elif form_status:
        #         if form_payment_state == 'Оплачена':
        #             print(form_payment_state, 'PAID')
        #             account.balance = account.balance - form_class.instance.amount
        #         elif form_payment_state != 'Оплачена':
        #             print(form_payment_state, 'NOPAID')
        #             account.balance = account.balance + form_class.instance.amount
        #     elif not form_status:
        #         account.balance = account.balance + form_class.instance.amount
        # elif type_of_form == 'create':
        #     if form_status and form_payment_state == 'Оплачена':
        #         account.balance = account - form_class.instance.amount
        account.save()



class InvoiceServiceForm(forms.ModelForm):
    use_required_attribute = False
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(InvoiceServiceForm, self).__init__(*args, **kwargs)
        self.fields['unit'].empty_label = 'Выберите...'
        self.fields['service'].empty_label = 'Выберите...'

    unit = forms.ModelChoiceField(queryset=Unit.objects.all(),
                                  label='Ед. изм.',
                                  widget=forms.Select(
                                      attrs={'class': 'form-select'}),
                                  # empty_label='Выберите...'
                                  required=False
                                  )
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     label='Услуга',
                                     # empty_label='Выберите...',
                                     widget=forms.Select(
                                         attrs={'class': 'form-select'}),
                                     required = False
                                     )
    invoice = forms.ModelChoiceField(queryset=models.Invoice.objects.all(),
                                     required=False)

    class Meta:
        model = models.InvoiceService
        exclude = ['id']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'total': 'Стоимость, грн.',
            'price': 'Цена за ед., грн.',
            'amount': 'Расход'
        }



InvoiceServiceFormset = modelformset_factory(models.InvoiceService,
                                             InvoiceServiceForm,
                                             fields='__all__', can_delete=True,
                                             extra=0)
