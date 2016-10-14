from models.models import db, Chat, User, Stp, Request, RequestState, Message, Section, Type, \
    RequestComment, StpRequest, StpSection
from models.scripts.create_dummy import create_section_struct, create_request_stage

def create():
    db.connect()
    db.create_tables(
        [Chat, User, Stp, Request, RequestState, Message, Section, Type, StpRequest, RequestComment, StpSection])
    create_section_struct()
    create_request_stage()


create()
