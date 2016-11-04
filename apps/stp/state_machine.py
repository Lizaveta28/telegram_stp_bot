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
        # {
        #     'trigger': 'requests_show',
        #     'source': ('stp_main_menu',),
        #     'dest': 'stp_requests_show',
        #     'prepare': [],
        #     'conditions': [],
        #     'before': ['_show_requests'],
        #     'after': ['_save_state'],
        # },
        {
            'trigger': 'start_chat',
            'source': ('*'),
            'dest': 'stp_chatting',
            'prepare': [],
            'conditions': [],
            'before': ['_set_chat'],
            'after': ['_save_state']
        },
        {
            'trigger': 'drop_request',
            'source': ('*'),
            'dest': 'stp_request_drop',
            'prepare': [],
            'conditions': [],
            'before': ['_drop_request'],
            'after': ['_save_state']
        },
        {
            'trigger': 'drop_request_comment',
            'source': ('stp_request_drop'),
            'dest': 'stp_request_drop_comment',
            'prepare': [],
            'conditions': [],
            'before': ['_drop_request_comment'],
            'after': ['_save_state']
        },

    ]
    states = ['stp_initial', 'stp_greeting', 'stp_main_menu', 'stp_requests_show', 'stp_active_requests',
              'stp_chatting', 'stp_request_drop', 'stp_request_drop_comment']

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
                                                                                # ["Мои завершенные запросы"]
                                                                                ])
        self.tb.send_message(self.chat, "Для продолжения выберите одну из команд под полем ввода.",
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
        stp = Stp.get(Stp.user == user)
        stp_sections = StpSection.select(StpSection.section).where(StpSection.stp == stp)
        requests = Request.select().where(Request.section << stp_sections).offset(page * REQUEST_PAGE_SIZE).limit(
            REQUEST_PAGE_SIZE + 1)
        if not custom_data:
            self.tb.send_message(self.chat, "Заявки:", reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                                             [[get_button(
                                                                                                 "В главное меню")]]))
        req_len = len(requests)
        for i in range(req_len):
            buttons = self.get_request_control_buttons(stp, requests[i].id)
            if req_len == REQUEST_PAGE_SIZE + 1 and req_len == i + 1:
                buttons.append([get_button_inline(text="Показать еще", data="stp_request_show %s" % (page + 1))])
            self.print_request(requests[i], stp=stp, keyboard=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons))

    def get_request_control_buttons(self, stp, request_id):
        buttons = []
        if not StpRequest.select().where(StpRequest.stp == stp.id and StpRequest.request == request_id).count():
            buttons.append([get_button_inline(text="Взять", data="stp_request_take %s" % request_id),
                            get_button_inline(text="Взять и начать чат",
                                              data="stp_request_take_and_chat %s" % request_id)])
        else:
            buttons.append([get_button_inline(text="Начать чат",
                                              data="stp_request_chat %s" % request_id),
                            get_button_inline(text="Отключиться от заявки",
                                              data="stp_request_dismiss_request %s" % request_id)
                            ])
        return buttons

    def print_request(self, request, keyboard, stp, reply=None):
        self.tb.send_message(self.chat,
                             "Заявка /r%s:\nНомер: %s\nНовых сообщений: <b>%s</b>\nКатегория: %s\nТип: %s\nКомментарий: %s\nСтатус: %s" % (
                                 str(request.id) + ' ' + request.unicode_icons,
                                 request.id,
                                 self.count_request_messages(request.id, stp),
                                 get_breadcrumb(request.type.section.id, Section, 'parent_section'),
                                 get_breadcrumb(request.type.id, Type, 'parent_type'),
                                 request.text,
                                 request.state.name
                             ), reply_markup=keyboard, parse_mode='HTML')

    def count_request_messages(self, id, stp):
        chats = Chat.select().where(Chat.request == id)
        return Message.select().where(Message.chat << chats).where(Message.is_read == False).where(
            Message.to_user == stp.id).count()

    def show_request(self, request_id, curr_user, reply=None):
        r = Request.get(id=request_id)
        buttons = []
        stp = Stp.get(Stp.user == curr_user)
        stp_sections = StpSection.select(StpSection.section).where(StpSection.stp == stp)
        is_suitable = Request.select().where(Request.section == r.section).where(
            Request.section << stp_sections).exists()
        if is_suitable:
            buttons = self.get_request_control_buttons(stp, request_id)
        self.print_request(r, keyboard=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons), stp=stp)

    def _set_chat(self, event):
        request = Request.get(id=event.kwargs.get('request'))
        user = event.kwargs.get("user")
        stp = Stp.get(user=user)
        stp_request = StpRequest.get_or_create(request=request, stp=stp)
        chat = Chat.get_or_create(request=request, user_to=None)[0]
        chat.user_to = stp.id
        chat.save()
        user.additional_data['chat'] = chat.id
        user.save()
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, [[get_button("Отключиться от чата")]])
        self.tb.send_message(self.chat,
                             "Вы переключились в чат заявки /r%s %s\n, имя клиента: %s\nФамилия клиента: %s\n" % (
                                 request.id, request.unicode_icons, request.user.first_name, request.user.surname),
                             reply_markup=keyboard)
        chats = Chat.select().where(Chat.request == request.id)
        for message in Message.select().where(Message.chat << chats).where(Message.is_read == False).where(Message.to_user==stp.id):
            message.is_read = True
            message.save()
            self.tb.send_message(self.chat, message.text)


    def send_to_chat_text(self, stp_user, message):
        chat = Chat.get(id=stp_user.additional_data['chat'])
        user = User.get(id=chat.user_from)
        request = Request.get(id=chat.request)
        if 'chat' in user.additional_data and chat.id == user.additional_data['chat']:
            Message(is_read=True, from_user=stp_user, to_user=user, text=message.text, chat=chat).save()
            self.tb.send_message(user.telegram_chat_id, "%s" % message.text)
        else:
            Message(is_read=False, from_user=stp_user, to_user=user, text=message.text, chat=chat).save()

    def take_request(self, request, user, call):
        stp = Stp.get(user=user)
        request = Request.get(id=request)
        stp_request, created = StpRequest.get_or_create(request=request, stp=stp)
        if created:
            self.tb.edit_message_reply_markup(self.chat, message_id=call.message.message_id,
                                              reply_markup=generate_custom_keyboard(types.InlineKeyboardMarkup,
                                                                                    self.get_request_control_buttons(
                                                                                        stp, request.id)))
        else:
            self.tb.send_message(self.chat, "Вы уже взяли заявку /r%s" % request.id)

    def _drop_request(self, event):
        r = Request.get(id=event.kwargs.get('request'))
        self.tb.send_message(self.chat,
                             "Вы хотите отключиться от заявки /r%s\nВы уверены? Так же вы можете добавить комментарий" % r.id,
                             reply_markup=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons=[
                                 [get_button_inline("Да", 'stp_request_drop_yes %s' % r.id),
                                  get_button_inline("Нет", 'stp_request_drop_no %s' % r.id)],
                                 [get_button_inline("Добавить комментарий к заявке\nи отключиться",
                                                    "stp_request_drop_comment %s" % r.id)]]))

    def drop_request_finally(self, message_id, request_id, user, decision, comment=None):
        if comment:
            self.tb.send_message(self.chat, "Вы добавили комментарий к заявке")
            request_id = user.additional_data['request']
            self.tb.send_message(self.chat, "Вы отключились от заявки /r%s" % request_id)
        else:
            if decision == 0:
                self.tb.edit_message_text("Вы остались подписаны на заявку /r%s" % request_id, chat_id=self.chat,
                                          message_id=message_id)
            else:
                self.tb.edit_message_text("Вы отключились от заявки /r%s" % request_id, chat_id=self.chat,
                                          message_id=message_id)

    def _drop_request_comment(self, event):
        user = event.kwargs.get('user')
        user.additional_data['request'] = event.kwargs.get('request_id')
        user.save()
        self.tb.send_message(self.chat,
                             'Укажите комментарий(причину)отключения от заявки, для отмены нажмите "В главное меню"',
                             reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                   [[get_button("В главное меню")]]))
