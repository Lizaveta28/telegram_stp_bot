from peewee import *
from playhouse.postgres_ext import JSONField, PostgresqlExtDatabase
from playhouse.fields import ManyToManyField
import datetime
from config import host, db, user, password

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

class Section(BaseModel):
    name = TextField()
    click_count = IntegerField(default=0)
    parent_section = ForeignKeyField('self', null=True, related_name='children')


class Type(BaseModel):
    name = TextField()
    click_count = IntegerField(default=0)
    comment_required = BooleanField(default=False)
    section = ForeignKeyField(Section, null=True)
    parent_type = ForeignKeyField('self', null=True, related_name='children')


class RequestState(BaseModel):
    name = TextField()


class Request(BaseModel):
    section = ForeignKeyField(Section)
    type = ForeignKeyField(Type)
    text = TextField(null=True)
    state = ForeignKeyField(RequestState)
    user = ForeignKeyField(User)
    unicode_icons = CharField(max_length=4)
    created_at = DateTimeField(default=datetime.datetime.now())


class Chat(BaseModel):
    user_from = IntegerField(null=True) # client
    user_to = IntegerField(null=True) # stp
    request = ForeignKeyField(Request)


class Stp(BaseModel):
    staff_id = IntegerField(null=True)
    user = ForeignKeyField(User)
    is_active = BooleanField(default=True)
    # current_requests = ManyToManyField(Request, related_name='current_requests')


class Message(BaseModel):
    is_read = BooleanField(default=False)
    to_user = ForeignKeyField(User, related_name="msg_to_user")
    from_user = ForeignKeyField(User, related_name="msg_from_user")
    data = BlobField(null=True)
    text = TextField(null=True)
    chat = ForeignKeyField(Chat)


class RequestComment(BaseModel):
    text = TextField(null=True)
    rating = FloatField(default=1)
    date_start = DateTimeField()
    date_finished = DateTimeField(datetime.datetime.now())


class StpRequest(BaseModel):
    request = ForeignKeyField(Request)
    stp = ForeignKeyField(Stp)
    comment = ForeignKeyField(RequestComment, null=True)
    add_text = TextField(null=True)
    is_important = BooleanField(default=False)


class StpSection(BaseModel):
    stp = ForeignKeyField(Stp)
    section = ForeignKeyField(Section)
    importance = IntegerField(default=1) # more is more prior
