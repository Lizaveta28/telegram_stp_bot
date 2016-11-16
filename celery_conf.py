from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from models.models import User, Request, Message
import telebot
import config
from state_machines.utils import *

app = Celery('tasks')
app.conf.update(
    BROKER_URL='redis://localhost',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERYBEAT_SCHEDULE={
        'save_page': {
            'task': 'tasks.check_messages',
            'schedule': 60.0,
        }
    }
)

tb = telebot.TeleBot(config.token)


def check_messages():
    notify_users = Message.select(Message.to_user).distinct().where(Message.is_read == False)
    for message in notify_users:
        if message.to_user.has_messages_after_notification:
            user = message.to_user
            user.has_messages_after_notification = False
            user.save()
            tb.send_message(message.to_user.telegram_chat_id, "Появились новые сообщения для завки(ок)")
