from models.models import User, Chat, Message, Request, Section, Type
from telebot import TeleBot
import config
from apps.simple_user.utils import get_breadcrumb
from state_machines.utils import *
from celery_conf import app
tb = TeleBot(config.token)


@app.task()
def message_notify():
    data_to_send = {}
    for chat in Chat.select():
        count = Message.select().where(Message.chat == chat.id).count()
        if count > 0:
            if not chat.user_from in data_to_send:
                data_to_send[chat.user_from] = []
            data_to_send[chat.user_from].append({'chat': chat.id,
                                                 'message_count': count})
    _notify_user(data_to_send)


def _notify_user(data):
    text = "Для ваших заявок есть новые сообщения:\n"
    keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup, [[get_button_inline("Мои заявки", "show_requests")]])
    for user_id in data:
        user = User.get(id=user_id)
        if user.has_messages_after_notification:
            for chat in data[user_id]:
                request = Request.get()
                text += "Заявка /r%s:\nНомер: %s\n<b>Новых сообщений:" \
                        "%s</b>\nКатегория: %s\nТип: %s\nКомментарий: %s\n" % (
                            str(request.id) + ' ' + request.unicode_icons,
                            request.id,
                            chat['message_count'],
                            get_breadcrumb(request.type.section.id, Section, 'parent_section'),
                            get_breadcrumb(request.type.id, Type, 'parent_type'),
                            request.text)
            tb.send_message(user.telegram_chat_id, text, reply_markup=keyboard, parse_mode='HTML')
            user.has_messages_after_notification = False
            user.save()
