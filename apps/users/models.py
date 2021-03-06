import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import signals

from apps.city.models import City
from .api.utilits import get_temperature
from .managers import CustomUserManager
from .validators import validate_phone


class User(AbstractUser):
    username = models.CharField('Имя пользователя', unique=True, null=True,
                                blank=True, max_length=25)
    email = models.EmailField('Электронная почта', unique=True)
    surname = models.CharField("Отчество", max_length=25, null=True,
                               blank=True)
    city = models.CharField('Город', max_length=75, null=True, blank=True)
    tg_id = models.CharField('Телеграм ID', max_length=155, null=True,
                             blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()
    phone = models.CharField('Номер телефона', max_length=13,
                             validators=[validate_phone], null=True)

    def __str__(self):
        if self.first_name == '' and self.last_name == '':
            return self.get_full_name()
        return self.username

    def get_full_name(self):
        full_name = f'{self.last_name} {self.first_name} {self.surname}'
        return full_name.strip().title()

    def get_phone(self):
        return f'+375{self.phone}'


class TokenTelegramBot(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='users_bot')
    code = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Токен для ТГ бота'
        verbose_name_plural = 'Токены для ТГ бота'

    def save(self, *args, **kwargs):
        self.code = ''.join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase,
                           k=15))
        super(TokenTelegramBot, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.code}'


def city_save(sender, instance, signal, *args, **kwargs):
    try:
        if instance.city:
            city, created = City.objects.get_or_create(name=instance.city)
            if created:
                city.name = instance.city,
                city.country = get_temperature(instance.city)['country'],
                city.count_users = 1
            else:
                city.count_users += 1
                city.save()
    except Exception:
        pass


signals.post_save.connect(city_save, sender=User)
