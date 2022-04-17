from celery import shared_task

from apps.users.management.commands.bot import send_message_for_user
from apps.users.models import User


@shared_task
def get_send_message():
    users = User.objects.all()
    for user in users:
        if user.tg_id and user.city:
            return send_message_for_user(user.tg_id, user.city)
