from models.models import db, Chat, User, Stp, Request, RequestState, Message, Section, Type, RequestChat, \
    RequestComment, StpRequest, StpSection


def create():
    db.connect()
    db.create_tables(
        [Chat, User, Stp, Request, RequestState, Message, Section, Type, RequestChat, StpRequest, RequestComment,
         StpSection])


create()
