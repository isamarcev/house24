import datetime

from django.db import models
from users.models import CustomUser
from crm_home.models import Tariff, Service, Unit, PaymentState
from home24 import settings


def get_next_transaction():
    ''' Getiing next number of transaction '''
    try:
        number_list = Transaction.objects.all().order_by('-number').\
            values('number')
        values_list = list()
        for item in number_list:
            values_list.append(item['number'])

        def check_instance(numbers, values, step=1):
            new_number = str(int(numbers[0]['number']) + step).zfill(11)
            if new_number in values:
                step += 1
                check_instance(numbers, values, step)
            else:
                return new_number
        return check_instance(number_list, values_list)
    except IndexError:
        new_number = str(1).zfill(11)
        return new_number


def get_next_account(count=None):
    """ Getiing next number of account """
    if not count:
        try:
            number = PersonalAccount.objects.order_by('-account_number')[0]
            return str(int(number.account_number) + 1).zfill(11)
        except IndexError:
            return str(1).zfill(11)
    else:
        numbers = PersonalAccount.objects.order_by('-account_number')[0]
        account_list = []
        for number in range(1, count):
            account_list.append(str(int(numbers.account_number) + number).zfill(11))
        return account_list


class PersonalAccount(models.Model):
    account_number = models.CharField(default=get_next_account, unique=True,
                                      max_length=14)
    house = models.ForeignKey("houses.House", on_delete=models.CASCADE,
                              null=True, blank=True)
    section = models.ForeignKey('houses.Section', on_delete=models.SET_NULL,
                                null=True, blank=True)
    flat = models.ForeignKey('houses.Flat', on_delete=models.SET_NULL,
                             null=True, blank=True)
    status_choice = [('active', "Активен"), ('nonactive', "Неактивен")]
    status = models.CharField(choices=status_choice, null=True, blank=True,
                              max_length=20)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    class Meta:
        verbose_name_plural = "Персональные счета"
        verbose_name = "Персональный счет"

    def __str__(self):
        return str(self.account_number)




def get_next_invoice():
    ''' Getiing next number of transaction '''
    try:
        number_list = Invoice.objects.all().order_by('-number'). \
            values('number')
        values_list = list()
        for item in number_list:
            values_list.append(item['number'])
        def check_instance(numbers, values, step=1):
            new_number = str(int(numbers[0]['number']) + step).zfill(11)
            if new_number in values:
                step += 1
                check_instance(numbers, values, step)
            else:
                return new_number

        return check_instance(number_list, values_list)
    except IndexError:
        new_number = str(1).zfill(11)
        return new_number


status_invoice = [('', 'Выберите...'),
                  ('Оплачена', 'Оплачена'),
                  ('Частично оплачена', 'Частично оплачена'),
                  ('Неоплачена', 'Неоплачена')]


class Invoice(models.Model):
    number = models.CharField(unique=True, default=get_next_invoice,
                              max_length=15)
    date = models.DateField(default=datetime.datetime.now)
    house = models.ForeignKey('houses.House', on_delete=models.CASCADE)
    section = models.ForeignKey('houses.Section', on_delete=models.CASCADE)
    flat = models.ForeignKey('houses.Flat', on_delete=models.CASCADE)
    personal_account = models.CharField(max_length=50, null=True, blank=True)
    payment_state = models.BooleanField(verbose_name='Проведена',
                                        null=True, blank=True)
    status = models.CharField(max_length=120,
                              choices=status_invoice,
                              null=True,
                              default="Неоплачена",
                              blank=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT)
    period_start = models.DateField(default=datetime.datetime.now)
    period_end = models.DateField(default=datetime.datetime.now)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name_plural = 'Квитанции'
        verbose_name = 'Квитанция'

    def __str__(self):
        return self.number


class Transaction(models.Model):
    number = models.CharField(default=get_next_transaction, max_length=15)
    date = models.DateField(default=datetime.datetime.now)
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                              related_name='owner', null=True, blank=True)
    personal_account = models.ForeignKey(PersonalAccount,
                                         on_delete=models.PROTECT,
                                         null=True, blank=True)
    payment_state = models.ForeignKey(PaymentState, on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    completed = models.BooleanField(null=True, blank=True, default=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.PROTECT,
                                null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name_plural = 'Транзакции'
        verbose_name = 'Транзакция'


class InvoiceService(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True,
                                blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, null=True,
                                 blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=10, null=True,
                                blank=True)

    def __str__(self):
        return f'{self.invoice} {self.service}'

    class Meta:
        verbose_name_plural = 'Квитанции с услугами'
        verbose_name = 'Квитанция с услугами'

