from django.db import models

from crm_accounting.models import PersonalAccount
from crm_home.models import Tariff
from users.models import CustomUser


class House(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image_1 = models.ImageField(upload_to='house/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='house/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='house/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='house/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='house/', null=True, blank=True)
    users = models.ManyToManyField(CustomUser)

    class Meta:
        verbose_name_plural = 'Дома'
        verbose_name = 'Дом'

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Секции'
        verbose_name = 'Секция'

    def __str__(self):
        return f'{self.title}'


class Floor(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True)


    class Meta:
        verbose_name_plural = 'Этажи'
        verbose_name = 'Этаж'

    def __str__(self):
        return self.title


class Flat(models.Model):
    number = models.IntegerField()
    area = models.FloatField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, error_messages={'required': 'Это поле обязательно.'})
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True,)
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True,)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, null=True, blank=True,)
    personal_account = models.OneToOneField(PersonalAccount, on_delete=models.CASCADE, related_name='account_flat',
                                            null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Квартиры'
        verbose_name = 'Квартира'

    def __str__(self):
        return f'№{self.number}, {self.house}'