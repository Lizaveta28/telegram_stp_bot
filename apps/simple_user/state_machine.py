from transitions import Machine
from config import PAGE_SIZE, IS_PROD, CHAT_PAGE_SIZE
from models.models import User, Section, Type, Request, Message, Stp
import ujson
from apps.simple_user.utils import get_breadcrumb, emoji_pool
import datetime
import random
from state_machines.utils import *


class UserStateMachine(object):
    mach_transitions = [
        {
            'trigger': 'greet',
            'source': ('initial',),
            'dest': 'greeting',
            'prepare': [],
            'conditions': [],
            'before': ['_greet'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'main_menu',
            'source': ('*'),
            'dest': 'main_menu',
            'prepare': [],
            'conditions': [],
            'before': ['_main_menu'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'select_section',
            'source': (
                'main_menu', 'type_select', 'message_enter', 'section_select', 'message_entered', 'request_confirm'),
            'dest': 'section_select',
            'prepare': [],
            'conditions': [],
            'before': ['_show_sections'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'select_type',
            'source': ('section_select', 'type_select', 'message_enter', 'message_entered', 'request_confirm'),
            'dest': 'type_select',
            'prepare': [],
            'conditions': [],
            'before': ['_show_types'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'add_comment',
            'source': ('message_enter', 'type_select', 'message_entered', 'request_confirm'),
            'dest': 'message_enter',
            'prepare': [],
            'conditions': [],
            'before': ['_add_comment'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'confirm_request',
            'source': ('message_enter', 'type_select', 'request_confirm'),
            'dest': 'request_confirm',
            'prepare': [],
            'conditions': ['_check_comment'],
            'before': ['_show_request'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'send_request',
            'source': ('request_confirm',),
            'dest': 'request_sent',
            'prepare': [],
            'conditions': [],
            'before': ['_send_request'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'select_chat',
            'source': ('*'),
            'dest': 'chatting',
            'prepare': [],
            'conditions': ['_request_active'],
            'before': ['_select_chat'],
            'after': ['_save_state'],
        },
        {
            'trigger': 'end_request',
            'source': ('chatting',),
            'dest': 'main_menu',
            'before': ['_end_request'],
            'after': ['_save_state']
        }

    ]
    states = ['initial', 'greeting', 'main_menu', 'section_select', 'type_select', 'message_enter', 'message_entered',
              'conversation', 'request_sent', 'request_confirm',
              'request_ended', 'requests_show', 'chatting']

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
        self.tb.send_message(self.chat, 'Добро пожаловать, Вас приветствует служба поддержки "Строительный двор".')

    def _request_active(self, event):
        r = Request.get(id=event.kwargs.get('chat'))
        message = message = event.kwargs.get('message')
        if r.is_finished:
            self.tb.edit_message_text(chat_id=self.chat, text="<code>Данная заявка уже решена.</code>",
                                      message_id=message, parse_mode='HTML')
            return False
        else:
            return True

    def _main_menu(self, event):
        user = User.get(id=self.user)
        user.additional_data = {}
        user.save()
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, buttons=[["Создать заявку"],
                                                                                ["Мои заявки"]])
        self.tb.send_message(self.chat, "Для продолжения выберите одну из команд под полем ввода.",
                             reply_markup=keyboard)

    def _save_state(self, event):
        if self.user:
            user = User.get(id=self.user)
            user.state = self.state
            user.save()

    def _show_sections(self, event, custom_data=None):
        page = 0
        selected_section = None
        reply_message = None
        if custom_data:
            page = custom_data.get('page', 0)
            selected_section = custom_data.get('selected_section', None)
            if not selected_section:
                selected_section = None
            reply_message = custom_data.get('message_id', None)
        sections = Section.select().where(Section.parent_section == selected_section).order_by(
            Section.click_count.desc()).offset(page * PAGE_SIZE).limit(
            PAGE_SIZE)
        total_count = Section.select().where(Section.parent_section == selected_section).offset(
            page * PAGE_SIZE).count()
        if reply_message is None:
            keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, [['В главное меню']])
            self.tb.send_message(self.chat, "Выберите раздел, к которому относится вопрос:", reply_markup=keyboard)
        buttons = []
        for section in sections:
            if not IS_PROD:
                buttons.append(
                    [get_button_inline(section.name, "section_select %s" % section.id)])
            else:
                buttons.append(
                    [get_button_inline(section.name, "section_select %s" % section.id)])
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                get_button_inline("<", "section_prev %s %s" % (page - 1, selected_section if selected_section else '')))
        if selected_section:
            nav_buttons.append(
                get_button_inline("На уровень выше", "section_up %s" % selected_section if selected_section else ''))
        if total_count > PAGE_SIZE:
            nav_buttons.append(
                get_button_inline(">", "section_next %s %s" % (page + 1, selected_section if selected_section else '')))
        buttons.append(nav_buttons)
        keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup, buttons)
        if reply_message is None:
            if sections:
                self.tb.send_message(self.chat, "Доступные категории:", reply_markup=keyboard)
            else:
                self.tb.send_message(self.chat,
                                     "Доступные категории:\nКажется у данной категории нет доступных подкатегорий")
        else:
            if sections:
                self.tb.edit_message_reply_markup(self.chat, message_id=reply_message, reply_markup=keyboard)

    def save_selected_section(self, section, message):
        user = User.get(id=self.user)
        user.additional_data = dict()
        user.additional_data['section'] = section
        bread = get_breadcrumb(section, Section, 'parent_section')
        self.tb.edit_message_text("Вы выбрали раздел: %s" % bread, chat_id=self.chat,
                                  message_id=message)
        keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup,
                                            [[get_button_inline("Изменить", "section_change")]])
        self.tb.edit_message_reply_markup(self.chat, message_id=message, reply_markup=keyboard)
        user.save()

    def _show_types(self, event, custom_data=None):
        user = User.get(id=self.user)
        page = 0
        selected_type = None
        reply_message = None
        if custom_data:
            page = custom_data.get('page', 0)
            selected_type = custom_data.get('selected_type', None)
            if not selected_type:
                selected_type = None
            reply_message = custom_data.get('message_id', None)
        av_types = Type.select().where(
            Type.section == user.additional_data['section']).where(Type.parent_type == selected_type).order_by(
            Type.click_count.desc()).offset(
            page * PAGE_SIZE).limit(
            PAGE_SIZE)
        total_count = Type.select().where(
            Type.section == user.additional_data['section']).where(Type.parent_type == selected_type).offset(
            page * PAGE_SIZE).count()
        if reply_message is None:
            keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, [['В главное меню']])
            self.tb.send_message(self.chat, "Выберите тип вопроса:", reply_markup=keyboard)
        buttons = []
        for type in av_types:
            buttons.append([get_button_inline(type.name, "type_select %s" % type.id)])
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                get_button_inline("<", "type_prev %s %s" % (page - 1, selected_type if selected_type else '')))
        if selected_type:
            nav_buttons.append(
                get_button_inline("На уровень выше", "type_up %s" % selected_type if selected_type else ''))
        if total_count > PAGE_SIZE:
            nav_buttons.append(
                get_button_inline(">", "type_next %s %s" % (page + 1, selected_type if selected_type else '')))
        buttons.append(nav_buttons)
        keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup, buttons)
        if reply_message is None:
            if av_types:
                self.tb.send_message(self.chat, "Доступные типы вопросов:", reply_markup=keyboard)
            else:
                self.tb.send_message(self.chat,
                                     "Доступные типы вопросов:\nКажется у данного типа или категории нет доступных типов обращений")
        else:
            self.tb.edit_message_reply_markup(self.chat, message_id=reply_message, reply_markup=keyboard)

    def save_selected_type(self, type, message):
        user = User.get(id=self.user)
        user.additional_data['type'] = type
        bread = get_breadcrumb(type, Type, 'parent_type')
        self.tb.edit_message_text("Вы выбрали тип вопроса: %s" % bread, chat_id=self.chat,
                                  message_id=message)
        keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup,
                                            [[get_button_inline("Изменить", "type_change")]])
        self.tb.edit_message_reply_markup(self.chat, message_id=message, reply_markup=keyboard)
        user.save()

    def _add_comment(self, event):
        user = User.get(id=self.user)
        self.tb.send_message(self.chat, "Введите описание вашего запроса:")

    def _check_comment(self, event):
        user = User.get(id=self.user)
        sel_type = Type.get(id=user.additional_data['type'])
        if sel_type.comment_required:
            if user.additional_data.get('comment', None) is None:
                return False
            else:
                return True
        else:
            return True

    def _show_request(self, event):
        user = User.get(id=self.user)
        sel_type = Type.get(id=user.additional_data['type'])
        sel_section = Section.get(id=user.additional_data['section'])
        text = "<b>Категория заявки</b>: %s\n<b>Тип заявки</b>: %s\n" % (sel_section.name, sel_type.name)
        comment = user.additional_data.get('comment', '')
        text += "<b>Комментарий</b>: %s" % comment
        keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup,
                                            [[get_button_inline("Изменить комментарий", "comment_change")],
                                             [get_button_inline("Изменить категорию", "section_change")],
                                             [get_button_inline("Изменить тип", "type_change")],
                                             [get_button_inline("Отправить обращение", "save_request")]])
        self.tb.send_message(self.chat, text, reply_markup=keyboard, parse_mode='HTML')

    def _save_comment(self, comment):
        user = User.get(id=self.user)
        user.additional_data['comment'] = comment
        user.save()

    def _send_request(self, event):
        message_id = event.kwargs.get('message_id')
        user = event.kwargs.get('user')
        request = Request()
        request.text = user.additional_data.get('comment', '')
        request.type = Type.get(id=user.additional_data.get('type'))
        request.section = request.type.section
        request.created_at = datetime.datetime.now()
        request.user = user
        request.unicode_icons = ''.join([random.choice(emoji_pool) for x in range(3)])
        request.save()
        self.tb.edit_message_text(chat_id=self.chat, message_id=message_id, text="Заявка успешно создана.")
        self.tb.send_message(self.chat,
                             "Сейчас вы будете перенаправлены в главное меню.\nВ ближайшее время с вами свяжется оператор прямо в этом чате")

    def show_requests(self, user_id):
        requests = Request.select().where(Request.user == user_id).where(Request.is_finished == False)
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, [['В главное меню']])
        self.tb.send_message(self.chat, "Список заявок:", reply_markup=keyboard)
        if not requests:
            self.tb.send_message(self.chat, "Нету активных заявок.")
        for request in requests:
            self.print_request(request)

    def show_request(self, request_id, curr_user):
        try:
            r = Request.get(id=request_id)
            if r.user == curr_user:
                self.print_request(r)
            else:
                self.tb.send_message(self.chat, "Это не ваша заявка!")
        except:
            self.tb.send_message(self.chat, "Данная заявка не найдена")

    def print_request(self, request):
        if not request.is_finished:
            keyboard = generate_custom_keyboard(types.InlineKeyboardMarkup, [
                [get_button_inline("Перейти в чат", 'start_chat %s' % request.id)],
                [get_button_inline("Заявка решена", "change_request_status %s" % request.id)]])
        else:
            keyboard = None
        self.tb.send_message(self.chat,
                             "Заявка /r%s:\nНомер: %s\nНовых сообщений: <b>%s</b>\nКатегория: %s\nТип: %s\nКомментарий: %s\nСтатус: %s" % (
                                 str(request.id) + ' ' + request.unicode_icons,
                                 request.id,
                                 self.count_request_messages(request.id, User.get(id=request.user)),
                                 get_breadcrumb(request.type.section.id, Section, 'parent_section'),
                                 get_breadcrumb(request.type.id, Type, 'parent_type'),
                                 request.text,
                                 "Завершена" if request.is_finished else "Не завершена"
                             ), reply_markup=keyboard,
                             parse_mode='HTML')

    def count_request_messages(self, id, user):
        return Message.select().where(Message.request == id).where(Message.is_read == False).where(
            Message.to_user == user.id).count()

    def _select_chat(self, event):
        user = event.kwargs.get('user')
        message = event.kwargs.get('message')
        self.tb.edit_message_text(chat_id=self.chat, message_id=message, text="Вы выбрали данную заявку.")
        r = Request.get(id=event.kwargs.get('chat'))
        user.additional_data['chat'] = r.id
        user.save()
        self.tb.send_message(self.chat,
                             "Вы были переключены в чат заявки /r%s %s" % (r.id, r.unicode_icons),
                             reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                   [[get_button("Показать историю сообщений")],
                                                                    [get_button("Заявка решена")],
                                                                    [get_button("Отключиться от чата")]]))
        self._show_unread_messages(r)

    def _show_unread_messages(self, request):
        self.tb.send_message(self.chat, "<code>Пропущенные сообщения:</code>", parse_mode='HTML')
        messages = Message.select().where(Message.request == request.id).where(
            Message.to_user == request.user).where(Message.is_read == False).order_by(Message.id)
        for message in messages:
            message.is_read = True
            message.save()
            self.tb.send_message(self.chat, message.text)
        self.tb.send_message(self.chat, "<code>Конец пропущенных сообщений</code>", parse_mode='HTML')

    def send_to_chat(self, text, user):
        try:
            r = Request.get(id=user.additional_data['chat'])
            if r.stp is not None:
                stp = User.get(id=Stp.get(id=r.stp).user)
                m = Message(from_user=user, to_user=stp.id, text=text, request=r)
                if 'chat' in stp.additional_data and stp.additional_data['chat'] == r.id:
                    m.is_read = True

                    self.tb.send_message(stp.telegram_chat_id, m.text)
            else:
                m = Message(from_user=user, to_user=None, text=text, request=r)
            m.save()
        except Exception as e:
            pass

    def _show_request_history(self, request_id, page=0):
        r = Request.get(id=request_id)
        messages = Message.select().where(Message.request == request_id).offset(page * CHAT_PAGE_SIZE).limit(
            CHAT_PAGE_SIZE)
        req_len = len(messages)
        if req_len:
            for i in range(req_len):
                text = "<code>%s</code>\n%s" % (
                    "Вы" if r.user == messages[i].from_user else "Тех. поддежрка", messages[i].text)
                messages[i].is_read = True
                messages[i].save()
                if req_len == CHAT_PAGE_SIZE and req_len == i + 1:
                    self.tb.send_message(self.chat, text,
                                         reply_markup=generate_custom_keyboard(types.InlineKeyboardMarkup,
                                                                               [[get_button_inline(
                                                                                   "Следующие %s сообщений" % CHAT_PAGE_SIZE,
                                                                                   "next_chat_page %s" % (page + 1))]]),
                                         parse_mode='HTML')
                else:
                    self.tb.send_message(self.chat, text, parse_mode='HTML')
        else:
            self.tb.send_message(self.chat, "Отображены все сообщения")

    def _confirm_end(self, user, request=None, message=None):
        if request is None:
            request = user.additional_data.get('chat')
        r = Request.get(id=request)
        if r.is_finished:
            if message:
                self.tb.edit_message_text(chat_id=self.chat, text="<code>Данная заявка уже решена.</code>",
                                          message_id=message, parse_mode='HTML')
        else:
            self.tb.send_message(self.chat, "вы уверены, что данная заявка решена?",
                                 reply_markup=generate_custom_keyboard(types.InlineKeyboardMarkup, [
                                     [get_button_inline("Да", "request_solved_yes %s" % r.id),
                                      get_button_inline("Нет", "request_solved_no %s" % r.id)]]))

    def _end_request(self, event, custom_data=None):
        user = User.get(id=self.user)
        if custom_data is None:
            from_stp = event.kwargs.get('from_stp', False)
            message = event.kwargs.get('message')
            request = Request.get(id=user.additional_data.get('chat'))
        else:
            from_stp = custom_data.get('from_stp', False)
            message = custom_data.get('message')
            request = Request.get(id=custom_data.get('request'))
        request.is_finished = True
        request.save()
        if from_stp:
            self.tb.edit_message_text("Вы согласились закрыть заявку.", chat_id=self.chat,
                                      message_id=message)
        else:
            self.tb.edit_message_text("Вы закрыли данную заявку.", chat_id=self.chat,
                                      message_id=message)
        user_stp = request.stp.user
        if from_stp:
            self.tb.send_message(user_stp.telegram_chat_id, "Пользователь согласился закрыть заявку /r%s %s" % (request.id, request.unicode_icons))
        else:
            self.tb.send_message(user_stp.telegram_chat_id, "Пользователь закрыл заявку /r%s %s" % (request.id, request.unicode_icons))
        if user_stp.state == 'stp_chatting' and user_stp.additional_data.get('chat') == request.id:
            user_stp.state = 'stp_main_menu'
            user_stp.additional_data = {}
            user_stp.save()
            self.tb.send_message(user_stp.telegram_chat_id, "Сейчас вы будете переведены в главное меню",
                                 reply_markup=generate_custom_keyboard(types.ReplyKeyboardMarkup,
                                                                       [[get_button("Список запросов")],
                                                                        [get_button("Мои активные запросы")]]))

    def _keep_request(self, message, request=None, from_stp=False):
        if request and from_stp:
            r = Request.get(id=request)
            if r.stp is not None:
                user_stp = r.stp.user
                if user_stp.additional_data.get('chat', -1) == r.id:
                    self.tb.send_message(user_stp.telegram_chat_id, "Пользователь оставил активной заявку")
                else:
                    self.tb.send_message(user_stp.telegram_chat_id, "Пользователь оставил активной заявку /r%s %s" % (r.id, r.unicode_icons))
        self.tb.edit_message_text("Ваша заявка актуальна.", chat_id=self.chat,
                                  message_id=message)
