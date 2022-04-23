from django.db import models


class City(models.Model):
    count_users = models.IntegerField('Пользователи', default=0)
    name = models.CharField('Название', max_length=155)
    country = models.CharField('Страна', max_length=155)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    # def _get_created_model(self, city, country):

    def __str__(self):
        return self.name
