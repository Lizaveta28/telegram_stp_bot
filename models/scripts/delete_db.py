from models.models import db, Chat, User, Stp, Request, RequestState, Message, Section, Type, RequestChat, \
    RequestComment, StpRequest


def drop():
    db.connect()
    tables = [Chat, User, Stp, Request, RequestState, Message, Section, Type, RequestChat, StpRequest, RequestComment]
    for table in tables:
        try:
            db.drop_table(table)
        except Exception as e:
            print(e)


drop()
