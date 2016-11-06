from models.models import db, User, Stp, Request, Message, Section, Type, \
    RequestComment, StpRequest


def drop():
    db.connect()
    tables = [User, Stp, Request, Message, Section, Type, StpRequest, RequestComment]
    for table in tables:
        try:
            db.drop_table(table)
        except Exception as e:
            print(e)


drop()
