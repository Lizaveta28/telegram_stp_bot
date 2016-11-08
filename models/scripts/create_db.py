from models.models import db, User, Stp, Request, Message, Section, Type, \
    RequestComment, StpRequest, StpSection, SiteUser
from models.scripts.create_dummy import create_section_struct

def create():
    db.connect()
    db.create_tables(
        [User, Stp, Request, Message, Section, Type, RequestComment, StpRequest, StpSection, SiteUser])
    create_section_struct()


create()
