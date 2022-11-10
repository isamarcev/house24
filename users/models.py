import datetime
from django.utils.translation import gettext_lazy as _

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


def get_next_user_id():
    try:
        users = CustomUser.objects.filter(is_superuser=False).\
            order_by('-username')
        if users.exists():
            user_id = int(users.first().username) + 1
        else:
            user_id = 1
    except:
        user_id = 2
    return user_id


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=30, help_text='Отчество',
                                   null=True, blank=True, default='')
    phone = models.CharField(max_length=20, null=True, blank=True, default='')
    viber = models.CharField(max_length=20, null=True, blank=True, default='')
    telegram = models.CharField(max_length=20, null=True, blank=True,
                                default='')
    status_state = [('Активен', 'Активен'), ('Новый', 'Новый'),
                    ('Отключен', 'Отключен')]
    status = models.CharField(choices=status_state, default=status_state[1][0],
                              max_length=20, null=True, blank=True)
    username = models.IntegerField(verbose_name="User ID",
                                unique=True, help_text='Required',
                                error_messages=
                                {"unique":
                                     "Пользователь с таким ID уже существует."},
                                blank=True, null=True,
                                default=get_next_user_id)
    about = models.TextField(max_length=1000, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=True,
                             blank=True)

    def __str__(self):
        if self.father_name:
            return f'{self.first_name} {self.last_name} {self.father_name}'
        else:
            return f'{self.first_name} {self.last_name}'


class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    message_address_house_id = models.ForeignKey('houses.House',
                                                 on_delete=models.SET_NULL,
                                                 null=True, blank=True)
    message_address_section_id = models.ForeignKey('houses.Section',
                                                   on_delete=models.SET_NULL,
                                                   null=True, blank=True)
    message_address_floor_id = models.ForeignKey('houses.Floor',
                                                 on_delete=models.SET_NULL,
                                                 null=True, blank=True)
    message_address_flat_id = models.ForeignKey('houses.Flat',
                                                on_delete=models.SET,
                                                null=True, blank=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Request(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    time = models.TimeField(default=datetime.datetime.now)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='owner_request',
                              null=True)
    description = models.TextField(max_length=1999, blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    flat = models.ForeignKey('houses.Flat', on_delete=models.PROTECT)
    masters = [("Сантехник", "Сантехник"), ("Электрик", "Электрик"),
               ("Слесарь", "Слесарь"), ("Любой специалист", "Любой специалист")]
    type_master = models.CharField(choices=masters, default=masters[0][0],
                                   max_length=50)
    status_request = [("", "Выберите..."), ("Новое", "Новое"),
                      ("В работе", "В работе"), ("Выполнено", "Выполнено")]
    status = models.CharField(choices=status_request, max_length=50,
                              default=status_request[1][0])
    master = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MessageUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE)
    read = models.BooleanField(default=False, blank=True)

