from transitions import Machine
from config import PAGE_SIZE, IS_PROD
from models.models import User, Section, Type, Request, Chat, RequestState
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

    ]
    states = ['stp_initial', 'stp_greeting', 'stp_main_menu']

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
