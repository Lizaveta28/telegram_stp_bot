from models.models import User, Section, Type, Stp
from flask_admin.contrib.peewee import ModelView
from flask_admin import expose
import flask_login
from peewee import JOIN, JOIN_LEFT_OUTER
from flask import request, redirect, url_for


class PermissionView(ModelView):

    # def __init__(self, *args, **kwargs):
    #     super(ModelView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class UserAdmin(PermissionView):

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.name = 'Пользователи'

    list_template = 'custom_user_list.html'
    column_exclude_list = ['additional_data', 'telegram_chat_id', 'telegram_user_id',
                             'has_messages_after_notification', 'state']
    form_excluded_columns = ['additional_data', 'telegram_chat_id', 'telegram_user_id',
                             'has_messages_after_notification', 'state', 'surname', 'username', 'first_name']
    column_list = ['first_name', 'surname', 'username', 'phone', 'is_active', ]
    column_labels = dict(username='Имя пользователя телеграм', first_name='Имя', phone='Телефон', is_active="Доступ к боту", surname="Фамилия")
    column_searchable_list = (User.surname, User.username, User.first_name, User.phone)
    column_filters = (User.is_active,)
    form_args = {
        'username': {
            'label': 'Имя пользователя телеграм',
        },
        'first_name': {
            'label': 'Имя',
        },
        'phone': {
            'label': 'Телефон',
        },
        'is_active': {
            'label': 'Доступ к боту',
        },
        'surname': {
            'label': 'Фамилия',
        },
    }
    can_create = False
    can_edit = True
    can_delete = False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        def is_not_stp(id):
            return Stp.select().where(Stp.user==id).where(Stp.is_active==True).count() == 0
        self._template_args['is_not_stp'] = is_not_stp
        self._actions
        return super(UserAdmin, self).index_view()


class SectionAdmin(PermissionView):
    def __init__(self, *args, **kwargs):
        super(SectionAdmin, self).__init__(*args, **kwargs)
        self.name = 'Разделы'

    column_exclude_list = ['click_count']
    form_excluded_columns = ['click_count']
    name = 'test'
    column_list = ['name', 'parent_section']
    column_labels = dict(name='Название раздела', parent_section='Раздел-родитель')
    can_create = True
    can_edit = True
    can_delete = True
    form_args = {
        'name': {
            'label': 'Название раздела',
        },
        'parent_section': {
            'label': 'Раздел-родитель',
        },
    }


class TypeAdmin(PermissionView):
    def __init__(self, *args, **kwargs):
        super(TypeAdmin, self).__init__(*args, **kwargs)
        self.name = 'Типы заявок'

    column_exclude_list = ['click_count']
    form_excluded_columns = ['click_count']
    name = 'test'
    column_list = ['name', 'parent_type', 'section', 'comment_required']
    column_labels = dict(name='Название типа заявки', parent_type='Тип-родитель', section='Раздел',
                         comment_required='Обязательный комментарий')
    column_filters = (Type.comment_required,)
    can_create = True
    can_edit = True
    can_delete = True
    form_args = {
        'name': {
            'label': 'Название типа заявки',
        },
        'parent_type': {
            'label': 'Тип-родитель',
        },
        'section': {
            'label': 'Раздел',
        },
        'comment_required': {
            'label': 'Обязательный комментарий',
        },
    }


class StpAdmin(PermissionView):
    def __init__(self, *args, **kwargs):
        super(StpAdmin, self).__init__(*args, **kwargs)
        self.name = 'Консьержи'

    column_list = ['user', 'staff_id', 'is_active']
    form_excluded_columns = ['user']
    column_labels = dict(user='Пользователь', staff_id='Идентификатор внутри СД', is_active='Доступ к панели консьержа')
    form_args = {
        'is_active': {
            'label': 'Доступ к панели консьержа',
        },
        'staff_id': {
            'label': 'Идентификатор внутри СД',
        }
    }
    can_create = False
    can_edit = True
    can_delete = False


class StpSectionAdmin(PermissionView):
    def __init__(self, *args, **kwargs):
        super(StpSectionAdmin, self).__init__(*args, **kwargs)
        self.name = 'Разделы консьержей'

    column_list = ['stp', 'section', 'importance']
    column_labels = dict(stp='Консьерж', section='Раздел', importance='Важность заявки из этого раздела')
    can_create = True
    can_edit = True
    can_delete = True
    form_args = {
        'stp': {
            'label': 'Консьерж',
        },
        'section': {
            'label': 'Раздел',
        },
        'importance': {
            'label': 'Важность заявки из этого раздела',
        }
    }
