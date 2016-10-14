from transitions import Machine
from config import PAGE_SIZE, IS_PROD, REQUEST_PAGE_SIZE
from models.models import User, Section, Type, Request, Chat, RequestState, Stp, StpRequest, StpSection, Message
import ujson
from apps.simple_user.utils import get_breadcrumb, emoji_pool
import datetime
import random
from state_machines.utils import *


class StpStateMachine(object):
    mach_transitions = [
        {
            'trigger': 'greet',
            'source': ('stp_initial',),
            'dest': 'stp_greeting',
            'prepare': [],
            'conditions': [],
            'before': ['_greet'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'main_menu',
            'source': ('*'),
            'dest': 'stp_main_menu',
            'prepare': [],
            'conditions': [],
            'before': ['_main_menu'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'requests_show',
            'source': ('stp_main_menu',),
            'dest': 'stp_requests_show',
            'prepare': [],
            'conditions': [],
            'before': ['_show_requests'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'start_chat',
            'source': ('*'),
            'dest': 'stp_chatting',
            'prepare': [],
            'conditions': [],
            'before': ['_set_chat'],
            'after': ['_save_state']
        },

    ]
    states = ['stp_initial', 'stp_greeting', 'stp_main_menu', 'stp_requests_show', 'stp_active_requests',
              'stp_chatting']

    def __init__(self, data):
        self.machine = Machine(model=self, transitions=self.mach_transitions, states=self.states,
                               initial=data.get('state', 'initial'), send_event=True)
        self.chat = data['chat_id']
        self.tb = data['tb']
        # getting db user id
        self.user = data['user_id']
        # Field for retrieve staff id after successful phone verification
        self.staff_id = None

    def _greet(self, event):
        self.tb.send_message(self.chat, 'Добро пожаловать, Вы были переведены в раздел СТП данного бота.')

    def _main_menu(self, event):
        user = User.get(id=self.user)
        user.additional_data = {}
        user.save()
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, buttons=[["Список запросов"],
                                                                                ["Мои активные запросы"],
                                                                                ["Мои завершенные запросы"]])
        self.tb.send_message(self.chat, "Для продолжения выберете одну из команд под полем ввода.",
                             reply_markup=keyboard)

    def _save_state(self, event):
        if self.user:
            user = User.get(id=self.user)
            user.state = self.state
            user.save()
            self.tb.send_message(self.chat, "State: %s" % user.state)

    def _show_requests(self, event, custom_data=None):
        if custom_data:
            user = custom_data.get('user', None)
            page = custom_data.get('page', 0)
        else:
            user = event.kwargs.get('user')
            page = 0
        stp = Stp.select().where(Stp.user == user)
        stp_sections = StpSection.select(StpSection.section).where(StpSection.stp == stp)
        requests = Request.select().where(Request.section << stp_sections).offset(page * REQUEST_PAGE_SIZE).limit(
            REQUEST_PAGE_SIZE)
        if not custom_data:
            self.tb.send_message(self.chat, "Заявки:", reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                                             [[get_button(
                                                                                                 "В главное меню")]]))
        req_len = len(requests)
        for i in range(req_len):
            buttons = []
            buttons.append([get_button_inline(text="Взять", data="stp_request_take %s" % requests[i].id),
                            get_button_inline(text="Взять и начать чат",
                                              data="stp_request_take_and_chat %s" % requests[i].id)])
            if req_len == REQUEST_PAGE_SIZE and req_len == i + 1:
                buttons.append([get_button_inline(text="Показать еще", data="stp_request_show %s" % (page + 1))])
            self.print_request(requests[i], keyboard=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons))

    def print_request(self, request, keyboard):
        self.tb.send_message(self.chat,
                             "Заявка /r%s:\nНомер: %s\nНовых сообщений: <b>%s</b>\nКатегория: %s\nТип: %s\nКомментарий: %s\nСтатус: %s" % (
                                 str(request.id) + ' ' + request.unicode_icons,
                                 request.id,
                                 self.count_request_messages(request.id),
                                 get_breadcrumb(request.type.section.id, Section, 'parent_section'),
                                 get_breadcrumb(request.type.id, Type, 'parent_type'),
                                 request.text,
                                 request.state.name
                             ), reply_markup=keyboard, parse_mode='HTML')

    def count_request_messages(self, id):
        chats = Chat.select().where(Chat.request == id)
        return Message.select().where(Message.chat << chats).count()

    def show_request(self, request_id, curr_user):
        r = Request.get(id=request_id)
        self.print_request(r)

    def _set_chat(self, event):
        request = Request.get(id=event.kwargs.get('request'))
        user = event.kwargs.get("user")
        stp = Stp.get(user=user)
        stp_request = StpRequest.get_or_create(request=request, stp=stp)
        chat = Chat.get_or_create(request=request, user_from=request.user, user_to=stp.user)[0]
        user.additional_data['chat'] = chat.id
        user.save()
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, [[get_button("Отключиться от чата")]])
        self.tb.send_message(self.chat,
                             "Вы переключились в чат заявки /r%s %s\n, имя клиента: %s\nФамилия клиента: %s\n" % (
                                 request.id, request.unicode_icons, request.user.first_name, request.user.surname),
                             reply_markup=keyboard)

    def send_to_chat_text(self, stp_user, message):
        chat = Chat.get(id=stp_user.additional_data['chat'])
        user = User.get(id=chat.user_from)
        request = Request.get(id=chat.request)
        if 'chat' in user.additional_data and chat.id == user.additional_data['chat']:
            Message(is_read=True, from_user=stp_user, to_user=user, text=message.text, chat=chat).save()
            self.tb.send_message(user.telegram_chat_id, "/r%s %s\n%s" % (request.id, request.unicode_icons,
                                                                         message.text))
        else:
            Message(is_read=False, from_user=stp_user, to_user=user, text=message.text, chat=chat).save()
