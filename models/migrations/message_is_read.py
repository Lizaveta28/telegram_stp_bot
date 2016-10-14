# Click count and comment required migration
from models.migrations.migrator import migrator
from playhouse.migrate import *

is_read = BooleanField(default=False)

migrate(
    migrator.add_column('message', 'is_read', is_read),
)