from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from .validators import validate_phone


class User(AbstractUser):
    username = models.CharField('Имя пользователя', unique=True, null=True,
                                blank=True, max_length=25)
    email = models.EmailField('Электронная почта', unique=True)
    surname = models.CharField("Отчество", max_length=25, null=True,
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

    def save(self, *args, **kwargs):
        if self.phone[:4] != '+375':
            self.phone = f'+375{self.phone}'
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = f'{self.last_name} {self.first_name} {self.surname}'
        return full_name.strip().title()
