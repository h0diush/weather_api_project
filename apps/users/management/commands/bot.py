import telebot
from django.core.management.base import BaseCommand

from apps.users.api.utilits import get_temperature
from apps.users.models import TokenTelegramBot, User
from config.settings.development import TOKEN_BOT
from django.core.exceptions import ObjectDoesNotExist

bot = telebot.TeleBot(TOKEN_BOT)


def send_message_for_user(chat_id, city):
    temperature = get_temperature(city)
    answer = f' {city}. Температура:  {temperature["temperature"]} °C'
    bot.send_photo(
        chat_id,
        f'https://openweathermap.org/img/w/{temperature["icon"]}.png',
        caption=answer
    )


def _get_user_by_token(chat_id):
    user = User.objects.get(tg_id=chat_id)
    return user


@bot.message_handler(commands=['start'])
def start_message(message):
    text = ('Добро пожаловать, данный бот будет указывать Вам погоду\n' +
            f'Для авторизации, напишите /reg')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['reg'])
def reg_user(message):
    if User.objects.filter(tg_id=message.chat.id).exists():
        bot.send_message(
            message.chat.id,
            'Вы уже авторизованы\n/weather - посмотреть погуду,/delete - выйти'
        )
    else:
        bot.send_message(message.chat.id, 'Введите ключ')


@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        user = _get_user_by_token(message.chat.id)
        temperature = get_temperature(user.city)
        answer = f'''
            {user.city}. Температура:  {temperature['temperature']} °C
        '''
        bot.send_photo(
            user.tg_id,
            f'https://openweathermap.org/img/w/{temperature["icon"]}.png',
            caption=answer
        )
        # bot.send_message(user.tg_id, answer)
    except ObjectDoesNotExist:
        bot.send_message(message.chat.id, 'Вы не авторизованы')


@bot.message_handler(commands=['delete'])
def get_delete_token(message):
    try:
        user = _get_user_by_token(message.chat.id)
        token = TokenTelegramBot.objects.get(user=user)
        token.delete()
        user.tg_id = ''
        user.save()
        bot.send_message(
            message.chat.id,
            'До скорой встречи :)'
        )
    except ObjectDoesNotExist:
        bot.send_message(
            message.chat.id,
            'Вы не авторизованы.\nДля авторизации выполните команду /reg'
        )


@bot.message_handler(content_types='text')
def get_reg_user(message):
    user = TokenTelegramBot.objects.filter(code=message.text).first()
    if user:
        owner = User.objects.get(username=user.user.username)
        owner.tg_id = message.from_user.id
        owner.save()
        answer = f'''
            Вы авторизовались как {owner.username}
        '''
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден')


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        bot.polling()
