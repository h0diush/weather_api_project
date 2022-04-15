from django.core.management.base import BaseCommand

import telebot
from apps.users.models import User, TokenTelegramBot

bot = telebot.TeleBot('1919502199:AAE4zHw_Ffe5MDSDtB3EbfnzCbkW-61c6N0')


@bot.message_handler(commands=['start'])
def start_message(message):
    text = '''
        Добро пожаловать, данный бот будет указывать Вам погоду
        '''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['reg'])
def reg_user(message):
    bot.send_message(message.chat.id, 'Введите ключ')


@bot.message_handler(content_types='text')
def get_reg_user(message):
    user = TokenTelegramBot.objects.filter(code=message.text).first()
    if user:
        owner = User.objects.get(username=user.user.username)
        owner.tg_id = message.from_user.id
        owner.save()
        bot.send_message(message.chat.id, owner.username)
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден')


class Command(BaseCommand):
    help = 'Телеграмм бот'

    def handle(self, *args, **options):
        bot.polling()
