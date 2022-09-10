from django.db import models


class Unit(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=100)
    show = models.BooleanField(null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Tariff(models.Model):
    name = models.CharField(max_length=100, default='Test')
    describe = models.TextField(max_length=2000, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TariffService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name_plural = "Тарифы Услуги"
        verbose_name = "Тариф Услуга"


def get_next_counter_number():
    """ Getting next number of counter """
    number = CounterData.objects.order_by('number')[-1].number
    x = str(int(number) + 1).zfill(10)
    return x


class CounterData(models.Model):
    number = models.IntegerField(default=get_next_counter_number, editable=True)
    date = models.DateField(auto_now_add=True)
    house = models.ForeignKey('houses.House', on_delete=models.CASCADE)
    section = models.ForeignKey('houses.Section', on_delete=models.CASCADE)
    flat = models.ForeignKey('houses.Flat', on_delete=models.CASCADE)
    StatusCounter = [("Новое", "Новое"), ("Учтено", "Учтено"), ("Учтено и оплачено", "Учтено и оплачено"),
                     ("Нулевое", "Нулевое")]
    status = models.CharField(choices=StatusCounter,max_length=40)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    data = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.number


class Requisites(models.Model):
    title = models.CharField(max_length=100)
    info = models.TextField(max_length=1000)


class PaymentState(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(choices=[("Приход", "Приход"), ("Расход", "Расход")], max_length=30)
