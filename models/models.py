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
    type = ForeignKeyField(Type)
    text = TextField(null=True)
    state = ForeignKeyField(RequestState)
    user = ForeignKeyField(User)
    unicode_icons = CharField(max_length=4)
    created_at = DateTimeField(default=datetime.datetime.now())


class Chat(BaseModel):
    user_from = IntegerField()
    user_to = IntegerField()
    request = ForeignKeyField(Request)


class Stp(BaseModel):
    staff_id = IntegerField(null=True)
    user = ForeignKeyField(User)
    is_active = BooleanField(default=True)
    sections = ForeignKeyField(Section)
    # current_requests = ManyToManyField(Request, related_name='current_requests')


class Message(BaseModel):
    user = ForeignKeyField(User)
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