from django.db import models
from django.contrib.auth.models import AbstractUser
from home24 import settings
from django.apps import apps


class Role(models.Model):
    name = models.CharField(max_length=50)
    statistics = models.BooleanField(null=True, blank=True)
    cashbox = models.BooleanField(null=True, blank=True)
    invoice = models.BooleanField(null=True, blank=True)
    personal_account = models.BooleanField(null=True, blank=True)
    flat = models.BooleanField(null=True, blank=True)
    owner = models.BooleanField(null=True, blank=True)
    house = models.BooleanField(null=True, blank=True)
    message = models.BooleanField(null=True, blank=True)
    application = models.BooleanField(null=True, blank=True)
    meter = models.BooleanField(null=True, blank=True)
    site_management = models.BooleanField(null=True, blank=True)
    service = models.BooleanField(null=True, blank=True)
    tariff = models.BooleanField(null=True, blank=True)
    role = models.BooleanField(null=True, blank=True)
    users = models.BooleanField(null=True, blank=True)
    requisites = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=30, help_text='Отчество', null=True, blank=True, default='')
    phone = models.CharField(max_length=20, null=True, blank=True, default='')
    viber = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=20, null=True, blank=True)
    status_state = [('Активен', 'Активен'), ('Новый', 'Новый'), ('Отключен','Отключен')]
    status = models.CharField(choices=status_state, default=status_state[1][0], max_length=20)
    username = models.CharField(max_length=100, verbose_name="User ID", unique=True, help_text='Required',
                                error_messages={"unique": "Пользователь с таким ID уже существует."},
                                blank=True, null=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.father_name}'


class Message(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=120)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Request(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owner_transaction')
    description = models.TextField(max_length=1999, blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    flat = models.ForeignKey('houses.Flat', on_delete=models.PROTECT)
    masters = [("Сантехник", "Сантехник"), ("Электрик", "Электрик"), ("Любой специалист", "Любой специалист")]
    type_master = models.CharField(choices=masters, default=masters[0][0], max_length=50)
    status_request = [("Новое", "Новое"), ("В работе", "В работе"), ("Выполнено", "Выполнено")]
    status = models.CharField(choices=status_request, max_length=50)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class MessageUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE)


