# Click count and comment required migration
from models.migrations.migrator import migrator
from playhouse.migrate import *
from models.models import User

user = ForeignKeyField(User, default=1, to_field=User.id)

migrate(
    migrator.add_column('request', 'user_id', user),
)