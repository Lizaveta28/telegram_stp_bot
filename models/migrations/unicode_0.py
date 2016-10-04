# Click count and comment required migration
from models.migrations.migrator import migrator
from playhouse.migrate import *
from models.models import User

unicode_icons = CharField(max_length=4, default='')

migrate(
    migrator.add_column('request', 'unicode_icons', unicode_icons),
)