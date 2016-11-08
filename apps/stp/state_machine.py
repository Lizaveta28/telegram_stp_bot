from transitions import Machine
from config import PAGE_SIZE, IS_PROD, REQUEST_PAGE_SIZE
from models.models import User, Section, Type, Request, Stp, StpRequest, StpSection, Message
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
            'conditions': ['_is_taken'],
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
            stp_filter = custom_data.get('stp', None)
        else:
            stp_filter = None
            user = event.kwargs.get('user')
            page = 0
        stp = Stp.get(Stp.user == user)
        stp_sections = StpSection.select(StpSection.section).where(StpSection.stp == stp).where(Request.is_finished==False)
        requests = Request.select().where(Request.section << stp_sections)
        if stp_filter:
            requests = requests.where(Request.stp==stp_filter)
        else:
            requests = requests.where(Request.stp == None)
        requests = requests.offset(page * REQUEST_PAGE_SIZE).limit(
            REQUEST_PAGE_SIZE + 1)
        if not custom_data:
            self.tb.send_message(self.chat, "Заявки:", reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                                             [[get_button(
                                                                                                 "В главное меню")]]))
        req_len = len(requests)
        if req_len:
            for i in range(req_len):
                buttons = self.get_request_control_buttons(stp, requests[i].id)
                if req_len == REQUEST_PAGE_SIZE + 1 and req_len == i + 1:
                    buttons.append([get_button_inline(text="Показать еще", data="stp_request_show %s" % (page + 1))])
                self.print_request(requests[i], stp=stp,
                                   keyboard=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons))
        else:
            self.tb.send_message(self.chat, "Нету доступных заявок.")

    def get_request_control_buttons(self, stp, request_id):
        buttons = []
        r = Request.get(id=request_id)
        if not r.stp == stp:
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
        stp = User.get(id=stp.user)
        self.tb.send_message(self.chat,
                             "Заявка /r%s:\nНомер: %s\nНовых сообщений: <b>%s</b>\nКатегория: %s\nТип: %s\nКомментарий: %s" % (
                                 str(request.id) + ' ' + request.unicode_icons,
                                 request.id,
                                 self.count_request_messages(request, stp),
                                 get_breadcrumb(request.type.section.id, Section, 'parent_section'),
                                 get_breadcrumb(request.type.id, Type, 'parent_type'),
                                 request.text,
                             ), reply_markup=keyboard, parse_mode='HTML')

    def count_request_messages(self, request, stp):
        return Message.select().where(Message.request == request.id).where(Message.is_read == False).where(request.user.id==Message.from_user).count()

    def show_request(self, request_id, curr_user, reply=None):
        r = Request.get(id=request_id)
        buttons = []
        stp = Stp.get(Stp.user == curr_user)
        stp_sections = StpSection.select(StpSection.section).where(StpSection.stp == stp)
        is_suitable = Request.select().where(Request.section == r.section).where(
            Request.section << stp_sections).where(Request.is_finished==False).exists()
        if is_suitable:
            buttons = self.get_request_control_buttons(stp, request_id)
        self.print_request(r, keyboard=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons), stp=stp)

    def _set_chat(self, event):
        request = Request.get(id=event.kwargs.get('request'))
        user = event.kwargs.get("user")
        message = event.kwargs.get("message")
        stp = Stp.get(user=user)
        request.stp = stp
        request.save()
        user.additional_data['chat'] = request.id
        user.save()
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, [# [get_button("Показать историю чата")],
                                                                        # [get_button("Закрыть заявку")],
                                                                        # [get_button("Клиент в чате?")],
                                                                        [get_button("Отключиться от заявки")],
                                                                        [get_button("Отключиться от чата")]])
        self.tb.edit_message_text(chat_id=self.chat,
                             text="Вы переключились в чат заявки /r%s %s" % (request.id, request.unicode_icons), message_id=message)
        self.tb.send_message(self.chat, "имя клиента: %s\nФамилия клиента: %s\n" % (request.user.first_name, request.user.surname), reply_markup=keyboard)
        self._show_unread_messages(request)

    def _is_taken(self, event):
        request = Request.get(id=event.kwargs.get('request'))
        stp = Stp.get(user=event.kwargs.get("user"))
        if request.stp is None or request.stp==stp:
            return True
        else:
            self.tb.send_message(self.chat, "Данная заявка уже взята.")
            return False

    def send_to_chat_text(self, stp_user, message):
        r = Request.get(id=stp_user.additional_data['chat'])
        user = User.get(id=r.user)
        if 'chat' in user.additional_data and r.id == user.additional_data['chat']:
            Message(is_read=True, from_user=stp_user, to_user=user, text=message.text, request=r).save()
            self.tb.send_message(user.telegram_chat_id, "%s" % message.text)
        else:
            Message(is_read=False, from_user=stp_user, to_user=user, text=message.text, request=r).save()

    def take_request(self, request, user, call):
        stp = Stp.get(user=user)
        request = Request.get(id=request)
        if request.stp is None:
            request.stp = stp
            request.save()
            self.tb.edit_message_reply_markup(self.chat, message_id=call.message.message_id,
                                              reply_markup=generate_custom_keyboard(types.InlineKeyboardMarkup,
                                                                                    self.get_request_control_buttons(
                                                                                        stp, request.id)))
        else:
            self.tb.send_message(self.chat, "Вы уже взяли заявку, либо ее взял кто-то другой /r%s." % request.id)

    def _drop_request(self, event):
        r = Request.get(id=event.kwargs.get('request'))
        self.tb.send_message(self.chat,
                             "Вы хотите отключиться от заявки /r%s\nВы уверены? Так же вы можете добавить комментарий." % r.id,
                             reply_markup=generate_custom_keyboard(types.InlineKeyboardMarkup, buttons=[
                                 [get_button_inline("Да", 'stp_request_drop_yes %s' % r.id),
                                  get_button_inline("Нет", 'stp_request_drop_no %s' % r.id)],
                                 [get_button_inline("Добавить комментарий к заявке\nи отключиться",
                                                    "stp_request_drop_comment %s" % r.id)]]))

    def drop_request_finally(self, message_id, request_id, user, decision, comment=None):
        if comment:
            self.tb.send_message(self.chat, "Вы добавили комментарий к заявке.(Пока не сохраняется в бд)")
            request_id = user.additional_data.get('request')
            r = Request.get(id=request_id)
            r.stp = None
            r.save()
            self.tb.send_message(self.chat, "Вы отключились от заявки /r%s." % request_id)
        else:
            if decision == 0:
                self.tb.edit_message_text("Вы остались подписаны на заявку /r%s." % request_id, chat_id=self.chat,
                                          message_id=message_id)
            else:
                r = Request.get(id=request_id)
                r.stp = None
                r.save()
                self.tb.edit_message_text("Вы отключились от заявки /r%s." % request_id, chat_id=self.chat,
                                          message_id=message_id)

    def _show_unread_messages(self, request):
        messages = Message.select().where(Message.request == request.id).where(
            Message.from_user == request.user).where(Message.is_read==False).order_by(Message.id)
        for message in messages:
            message.to_user = request.stp.user
            message.is_read = True
            message.save()
            self.tb.send_message(self.chat, message.text)

    def _drop_request_comment(self, event):
        user = event.kwargs.get('user')
        user.additional_data['request'] = event.kwargs.get('request_id')
        user.save()
        self.tb.send_message(self.chat,
                             'Укажите комментарий(причину)отключения от заявки, для отмены нажмите "В главное меню".',
                             reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                   [[get_button("В главное меню")]]))
