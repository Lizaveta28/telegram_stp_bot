from peewee import *
from playhouse.postgres_ext import JSONField, PostgresqlExtDatabase
import datetime
from config import host, db, user, password
from apps.simple_user.utils import get_breadcrumb
from flask_peewee.auth import BaseUser


db = PostgresqlExtDatabase(db, user=user, password=password, host=host)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    telegram_user_id = IntegerField()
    telegram_chat_id = IntegerField()
    username = TextField(null=True)
    first_name = TextField(null=True)
    surname = TextField(null=True)
    additional_data = JSONField(null=True)
    state = TextField(default='initial')
    phone = TextField(null=True)
    is_active = BooleanField(default=True)
    has_messages_after_notification = BooleanField(default=False)

    def __unicode__(self):
        return "%s %s %s" % (self.username, self.first_name, self.surname)


class Section(BaseModel):
    name = TextField()
    click_count = IntegerField(default=0)
    parent_section = ForeignKeyField('self', null=True, related_name='children')

    def __unicode__(self):
        return get_breadcrumb(self.id, Section, 'parent_section')


class Type(BaseModel):
    name = TextField()
    click_count = IntegerField(default=0)
    comment_required = BooleanField(default=False)
    section = ForeignKeyField(Section, null=True)
    parent_type = ForeignKeyField('self', null=True, related_name='children')

    def __unicode__(self):
        return self.name


class Stp(BaseModel):
    staff_id = IntegerField(null=True)
    user = ForeignKeyField(User)
    is_active = BooleanField(default=True)

    # current_requests = ManyToManyField(Request, related_name='current_requests')

    def __unicode__(self):
        return self.user.__unicode__()


class Request(BaseModel):
    section = ForeignKeyField(Section)
    type = ForeignKeyField(Type)
    text = TextField(null=True)
    is_finished = BooleanField(default=False)
    rating = IntegerField(null=True)
    user = ForeignKeyField(User)
    stp = ForeignKeyField(Stp, null=True)
    unicode_icons = CharField(max_length=4)
    created_at = DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return "%s %s" % (self.section.name, self.type.name)


class Message(BaseModel):  # For show messages between stps and user
    is_read = BooleanField(default=False)
    to_user = ForeignKeyField(User, related_name="msg_to_user", null=True)
    from_user = ForeignKeyField(User, related_name="msg_from_user", null=True)
    data = BlobField(null=True)
    text = TextField(null=True)
    request = ForeignKeyField(Request)

    def __unicode__(self):
        return self.text


class RequestComment(BaseModel):
    text = TextField(null=True)
    rating = FloatField(default=1)
    date_start = DateTimeField()
    date_finished = DateTimeField(datetime.datetime.now())

    def __unicode__(self):
        return self.text


class StpRequest(BaseModel):
    request = ForeignKeyField(Request)
    stp = ForeignKeyField(Stp, null=True)
    user = ForeignKeyField(User, null=True)
    comment = ForeignKeyField(RequestComment, null=True)
    add_text = TextField(null=True)
    is_dissmised = BooleanField(default=False)
    is_important = BooleanField(default=False)

    def __unicode__(self):
        return self.comment


class StpSection(BaseModel):
    stp = ForeignKeyField(Stp)
    section = ForeignKeyField(Section)
    importance = IntegerField(default=1)  # more is more prior


class SiteUser(BaseModel, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    is_active = BooleanField(default=True)
    # ... our custom fields ...
    is_superuser = BooleanField(default=True)
    is_anonymous = BooleanField(default=False)
    is_authenticated = BooleanField(default=True)

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username
