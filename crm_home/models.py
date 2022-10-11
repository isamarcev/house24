import datetime

from django.db import models


class Unit(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=100)
    show = models.BooleanField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True,
                             blank=True)

    def __str__(self):
        return self.name


class Tariff(models.Model):
    name = models.CharField(max_length=100, error_messages=
                            {'required': 'Это поле обязательно к заполнению '
                                         'и не может быть пустым.'})
    describe = models.TextField(max_length=2000, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TariffService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True,
                                blank=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True,
                               blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True,
                                null=True, default=0)

    class Meta:
        verbose_name_plural = "Тарифы Услуги"
        verbose_name = "Тариф Услуга"

    # def clean_price(self):
    #     new_price = self.cleaned


def get_next_counter_number():
    """ Getting next number of counter """
    try:
        number = CounterData.objects.order_by('-id')[0].number
        x = str(int(number) + 1).zfill(10)
    except IndexError:
        x = str(1).zfill(10)
    return x


class CounterData(models.Model):
    number = models.CharField(default=get_next_counter_number, max_length=20,
                              unique=True)
    date = models.DateField(default=datetime.datetime.now)
    house = models.ForeignKey('houses.House', on_delete=models.CASCADE)
    section = models.ForeignKey('houses.Section', on_delete=models.CASCADE)
    flat = models.ForeignKey('houses.Flat', on_delete=models.CASCADE)
    StatusCounter = [("Новое", "Новое"), ("Учтено", "Учтено"),
                     ("Учтено и оплачено", "Учтено и оплачено"),
                     ("Нулевое", "Нулевое")]
    status = models.CharField(choices=StatusCounter, max_length=40)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    data = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.number)


class Requisites(models.Model):
    title = models.CharField(max_length=100)
    info = models.TextField(max_length=1000)


class PaymentState(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(choices=[("Приход", "Приход"),
                                     ("Расход", "Расход")],
                            max_length=30)
