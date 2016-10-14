# Click count and comment required migration
from models.migrations.migrator import migrator
from models.models import User
from playhouse.migrate import *

has_messages_after_notification = BooleanField(default=False)
to_user = ForeignKeyField(User, to_field=User.id, null=True)
from_user = ForeignKeyField(User, to_field=User.id, null=True)
migrate(
    migrator.add_column('user', 'has_messages_after_notification', has_messages_after_notification),
    migrator.add_column('message', 'to_user_id', to_user),
    migrator.add_column('message', 'from_user_id', from_user),
)