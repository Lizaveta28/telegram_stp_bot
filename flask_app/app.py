from flask import Flask

from flask_peewee.auth import Auth
from flask_peewee.db import Database
from models.models import User, Stp, Request, Message, Section, Type, RequestComment, StpRequest, StpSection, \
    SiteUser
from models.flask_models import UserShowAdmin, UserAdmin, CustomAuth, CustomAdmin, StpShowAdmin, RequestShowAdmin, \
    MessageShowAdmin, StpSectionShowAdmin

app = Flask(__name__)
app.config.from_object('flask_app.flask_config.Configuration')
db = Database(app)

# needed for authentication
auth = CustomAuth(app, db)
from flask_peewee.admin import Admin

admin = CustomAdmin(app, auth)
admin.register(SiteUser, UserAdmin)
admin.register(User, UserShowAdmin)
admin.register(Stp, StpShowAdmin)
admin.register(Request, RequestShowAdmin)
admin.register(Message, MessageShowAdmin)
admin.register(Section)
admin.register(Type)
admin.register(StpSection, StpSectionShowAdmin)
admin.setup()

if __name__ == "__main__":
    app.run()
